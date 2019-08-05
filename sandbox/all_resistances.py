#!/usr/bin/env python
# vim: set expandtab tabstop=4 shiftwidth=4:

import csv
import sys
from ftexplorer.data import Data, Weight

data = Data('BL2')

friendly_allegiances = {
        'GD_AI_Allegiance.Allegiance_Brick',
        'GD_AI_Allegiance.Allegiance_Player',
        'GD_AI_Allegiance.Allegiance_Player_NoLevel',
        'GD_AI_Allegiance.Allegiance_MissionNPC',
        'GD_AI_Allegiance.Allegiance_NPCNeutral',
        'GD_Anemone_AI_Allegiance.Allegiance_Anemone_Brick',
        }

def get_display_name(thing):
    """
    If the name has an equals sign in it, our processing stuff thinks it's
    a dict.  One of these days I should write a better processor for that.
    """
    if isinstance(thing, dict):
        new_name = '(error)'
        for key, val in thing.items():
            new_name = '{}={}'.format(key, val)
            break
        return new_name.strip('"')
    else:
        return thing.strip('"')

class Attribute(object):

    def __init__(self, name, report_dot, useless=False):
        self.name = name
        self.report_dot = report_dot
        self.useless = useless
        self.impact = None
        self.dot_damage = None
        self.dot_chance = None
        self.dot_duration = None

    def __eq__(self, other):
        """
        Note that this only checks values, not any of the metadata
        """
        return self.impact == other.impact \
                and self.dot_damage == other.dot_damage \
                and self.dot_chance == other.dot_chance \
                and self.dot_duration == other.dot_duration

    def is_interesting(self):
        return any([val is not None for val in [
            self.impact,
            self.dot_damage,
            self.dot_chance,
            self.dot_duration,
            ]])

    def get_labels(self):
        if self.useless:
            suffix = ' (does nothing)'
        else:
            suffix = ''
        labels = ['{} Impact Damage{}'.format(self.name, suffix)]
        if self.report_dot:
            labels.append('{} DOT Damage{}'.format(self.name, suffix))
            labels.append('{} DOT Chance{}'.format(self.name, suffix))
            labels.append('{} DOT Duration{}'.format(self.name, suffix))
        return labels

    def get_data(self):
        data = []

        if self.impact is None:
            data.append('')
        else:
            data.append(self.impact)

        if self.report_dot:

            if self.dot_damage is None:
                data.append('')
            else:
                data.append(self.dot_damage)

            if self.dot_chance is None:
                data.append('')
            else:
                data.append(self.dot_chance)

            if self.dot_duration is None:
                data.append('')
            else:
                data.append(self.dot_duration)

        return data

class AttributePair(object):

    def __init__(self, name, pt, pawnbalance, classdef, asv_dict,
            base_dot_chance=None, base_dot_duration=None,
            base_damage=None,
            mod_is_useless=False,
            mod_dot_chance=None, mod_dot_duration=None,
            mod_impact=None, mod_dot_damage=None,
            report_dot=True,
            report_base=True,
            ):
        self.name = name
        self.pt = pt
        self.report_dot = report_dot

        # Prep base stats
        self.base = Attribute(name, report_dot)
        if report_base:
            self.load_base(classdef, base_dot_chance, base_dot_duration, base_damage)

        # Prep modifiers!
        self.modifier = Attribute(name, report_dot, useless=mod_is_useless)
        self.load_modifier(asv_dict, mod_dot_chance, mod_dot_duration, mod_impact, mod_dot_damage)

    def __eq__(self, other):
        """
        Note that this only checks values, not any of the metadata
        """
        return self.base == other.base and self.modifier == other.modifier

    def load_base(self, classdef, base_dot_chance, base_dot_duration, base_damage):
        if self.report_dot:

            chance_val = Weight(classdef[base_dot_chance], self.pt).value
            if chance_val < 1:
                self.base.dot_chance = chance_val

            duration_val = Weight(classdef[base_dot_duration], self.pt).value
            if duration_val != 1:
                self.base.dot_duration = duration_val

        impact_val = Weight(classdef[base_damage]['ResistanceToImpact'], self.pt).value
        if impact_val != 1:
            self.base.impact = impact_val

        damage_val = Weight(classdef[base_damage]['ResistanceToStatusEffect'], self.pt).value
        if damage_val != 1:
            self.base.dot_damage = damage_val

    def load_modifier(self, asv_dict, mod_dot_chance, mod_dot_duration, mod_impact, mod_dot_damage):

        if mod_dot_chance in asv_dict and asv_dict[mod_dot_chance] < 1:
            self.modifier.dot_chance = asv_dict[mod_dot_chance]

        if mod_dot_duration in asv_dict and asv_dict[mod_dot_duration] != 1:
            self.modifier.dot_duration = asv_dict[mod_dot_duration]

        if mod_impact in asv_dict and asv_dict[mod_impact] != 1:
            self.modifier.impact = asv_dict[mod_impact]

        if mod_dot_damage in asv_dict and asv_dict[mod_dot_damage] != 1:
            self.modifier.dot_damage = asv_dict[mod_dot_damage]

    def is_interesting(self):
        return any([attr.is_interesting() for attr in [self.base, self.modifier]])

    def get_labels(self):
        labels = []
        for (blabel, mlabel) in zip(self.base.get_labels(), self.modifier.get_labels()):
            labels.append('Base {}'.format(blabel))
            labels.append('Modifier {}'.format(mlabel))
        return labels

    def get_data(self):
        data = []
        for (bdata, mdata) in zip(self.base.get_data(), self.modifier.get_data()):
            data.append(bdata)
            data.append(mdata)
        return data

class AttributeSet(object):

    def __init__(self, label, pawn_name, pt, pawnbalance, classdef):
        self.label = label
        self.pawn_name = pawn_name
        self.pt = pt
        self.pt_label = 'PT{}'.format(pt)

        # Create a combined AttributeStartingValues dict.
        # Technically the ASVs in AIPawnBalanceDefinition.PlayThroughs will override
        # values found in AIClassDefinitions.  In practice, this doesn't actually
        # happen anywhere in the BL2 data, or at least not for the vars we care about.
        # Still, we're technically supporting it here.
        asv_dict = {}
        if 'AttributeStartingValues' in classdef and classdef['AttributeStartingValues'] != '':
            AttributeSet.add_to_asv_dict(asv_dict, classdef['AttributeStartingValues'], idx+1)
        ptstruct = pawnbalance['PlayThroughs'][pt-1]
        if 'AttributeStartingValues' in ptstruct and ptstruct['AttributeStartingValues'] != '':
            AttributeSet.add_to_asv_dict(asv_dict, ptstruct['AttributeStartingValues'], idx+1)

        # Now define all our bits which provide resistance to things
        self.explosive = AttributePair('Explosive', pt, pawnbalance, classdef, asv_dict,
                base_damage='BaseExplosiveDamageModifiers',
                mod_impact='D_Attributes.DamageTypeModifers.ExplosiveImpactDamageModifier',
                report_dot=False,
                )
        self.grenade = AttributePair('Grenade', pt, pawnbalance, classdef, asv_dict,
                mod_impact='D_Attributes.DamageSourceModifiers.ReceivedGrenadeDamageModifier',
                report_dot=False,
                report_base=False,
                )
        self.melee = AttributePair('Melee', pt, pawnbalance, classdef, asv_dict,
                mod_impact='D_Attributes.DamageSourceModifiers.ReceivedMeleeDamageModifier',
                report_dot=False,
                report_base=False,
                )
        self.normal = AttributePair('Normal', pt, pawnbalance, classdef, asv_dict,
                base_damage='BaseNormalDamageModifiers',
                report_dot=False,
                )
        self.slag = AttributePair('Slag', pt, pawnbalance, classdef, asv_dict,
                base_dot_chance='BaseAmpChanceResistanceModifier',
                base_dot_duration='BaseAmpDurationResistanceModifier',
                base_damage='BaseAmpDamageModifiers',
                mod_is_useless=True,
                mod_dot_chance='D_Attributes.StatusEffectModifiers.AmpChanceResistanceModifier',
                mod_dot_duration='D_Attributes.StatusEffectModifiers.AmpDurationResistanceModifier',
                mod_impact='D_Attributes.DamageTypeModifers.AmpImpactDamageModifier',
                mod_dot_damage='D_Attributes.DamageTypeModifers.AmpStatusEffectDamageModifier',
                )
        self.corrosive = AttributePair('Corrosive', pt, pawnbalance, classdef, asv_dict,
                base_dot_chance='BaseCorrosiveChanceResistanceModifier',
                base_dot_duration='BaseCorrosiveDurationResistanceModifier',
                base_damage='BaseCorrosiveDamageModifiers',
                mod_is_useless=True,
                mod_dot_chance='D_Attributes.StatusEffectModifiers.CorrosiveChanceResistanceModifier',
                mod_dot_duration='D_Attributes.StatusEffectModifiers.CorrosiveDurationResistanceModifier',
                mod_impact='D_Attributes.DamageTypeModifers.CorrosiveImpactDamageModifier',
                mod_dot_damage='D_Attributes.DamageTypeModifers.CorrosiveStatusEffectDamageModifier',
                )
        self.fire = AttributePair('Fire', pt, pawnbalance, classdef, asv_dict,
                base_dot_chance='BaseIgniteChanceResistanceModifier',
                base_dot_duration='BaseIgniteDurationResistanceModifier',
                base_damage='BaseIncendiaryDamageModifiers',
                mod_is_useless=True,
                mod_dot_chance='D_Attributes.StatusEffectModifiers.IgniteChanceResistanceModifier',
                mod_dot_duration='D_Attributes.StatusEffectModifiers.IgniteDurationResistanceModifier',
                mod_impact='D_Attributes.DamageTypeModifers.IncendiaryImpactDamageModifier',
                mod_dot_damage='D_Attributes.DamageTypeModifers.IncendiaryStatusEffectDamageModifier',
                )
        self.shock = AttributePair('Shock', pt, pawnbalance, classdef, asv_dict,
                base_dot_chance='BaseShockChanceResistanceModifier',
                base_dot_duration='BaseShockDurationResistanceModifier',
                base_damage='BaseShockDamageModifiers',
                mod_is_useless=True,
                mod_dot_chance='D_Attributes.StatusEffectModifiers.ShockChanceResistanceModifier',
                mod_dot_duration='D_Attributes.StatusEffectModifiers.ShockDurationResistanceModifier',
                mod_impact='D_Attributes.DamageTypeModifers.ShockImpactDamageModifier',
                mod_dot_damage='D_Attributes.DamageTypeModifers.ShockStatusEffectDamageModifier',
                )

        # Get phaselockability
        self.disable_phaselock = None
        if 'DesignerFlagStartingValues' in classdef and classdef['DesignerFlagStartingValues'] != '':
            for dfsv in classdef['DesignerFlagStartingValues']:
                if 'GD_AI_Flags.Skills.Flag_Skills_DisablePhaseLock' in dfsv['FlagToSet']:
                    chance_val = Weight(dfsv['ChanceTrue'], pt=pt).value
                    if chance_val > 0:
                        if chance_val > 1:
                            self.disable_phaselock = 1
                        else:
                            self.disable_phaselock = chance_val

        # Get phaselock time scale
        pt_time = 'GD_Siren_Skills.Attributes.PhaselockTimeScale'
        if self.disable_phaselock is None and pt_time in asv_dict and asv_dict[pt_time] != 1:
            self.phaselock_time = asv_dict[pt_time]
        else:
            self.phaselock_time = None

    def __eq__(self, other):
        """
        Note that this only checks values, not any of the metadata
        """
        return self.explosive == other.explosive \
                and self.grenade == other.grenade \
                and self.melee == other.melee \
                and self.normal == other.normal \
                and self.slag == other.slag \
                and self.corrosive == other.corrosive \
                and self.fire == other.fire \
                and self.shock == other.shock \
                and self.disable_phaselock == other.disable_phaselock \
                and self.phaselock_time == other.phaselock_time

    def update_with_playthrough(self, other):
        self.pt_label = '{}+{}'.format(self.pt_label, other.pt_label)
        if self.label != other.label:
            self.label = '{}+{}'.format(self.label, other.label)

    @staticmethod
    def add_to_asv_dict(cur_dict, asv_list, pt):
        for asv in asv_list:
            name = Data.get_attr_obj(asv['Attribute'])
            cur_dict[name] = Weight(asv['BaseValue'], pt).value
        return cur_dict

    def is_interesting(self):
        return any([pair.is_interesting() for pair in [
                self.explosive,
                self.grenade,
                self.melee,
                self.normal,
                self.slag,
                self.corrosive,
                self.fire,
                self.shock,
            ]]) or self.phaselock_time is not None \
                    or self.disable_phaselock is not None

    def get_labels(self):
        labels = ['Pawn Balance', 'Playthrough', 'Name']
        labels.extend(self.normal.get_labels())
        labels.extend(self.melee.get_labels())
        labels.extend(self.explosive.get_labels())
        labels.extend(self.grenade.get_labels())
        labels.extend(['Disable Phaselock', 'Phaselock Time'])
        labels.extend(self.fire.get_labels())
        labels.extend(self.corrosive.get_labels())
        labels.extend(self.shock.get_labels())
        labels.extend(self.slag.get_labels())
        return labels

    def get_data(self):
        data = [self.pawn_name, self.pt_label, self.label]
        data.extend(self.normal.get_data())
        data.extend(self.melee.get_data())
        data.extend(self.explosive.get_data())
        data.extend(self.grenade.get_data())
        if self.disable_phaselock is None:
            data.append('')
        else:
            data.append(self.disable_phaselock)
        if self.phaselock_time is None:
            data.append('')
        else:
            data.append(self.phaselock_time)
        data.extend(self.fire.get_data())
        data.extend(self.corrosive.get_data())
        data.extend(self.shock.get_data())
        data.extend(self.slag.get_data())
        return data

startvals = {}
ret_list = []
shown_header = False
writer = csv.writer(sys.stdout)
for pawnbal_name in sorted(data.get_all_by_type('AIPawnBalanceDefinition')):
    pawnbal = data.get_struct_by_full_object(pawnbal_name)
    if 'PlayThroughs' in pawnbal:
        aipawn = data.get_struct_attr_obj_real(pawnbal, 'AIPawnArchetype')
        allegiance = Data.get_attr_obj(aipawn['Allegiance'])
        if allegiance not in friendly_allegiances:
            aiclass_name = Data.get_attr_obj(aipawn['AIClass'])
            aiclass = data.get_struct_attr_obj_real(aipawn, 'AIClass')

            # Loop through all playthroughs to gather stats
            pawn_stats = []
            for (idx, pt) in enumerate(pawnbal['PlayThroughs']):
                display_name = get_display_name(pt['DisplayName'])
                pawn_stats.append(AttributeSet(display_name, pawnbal_name, idx+1, pawnbal, aiclass))

            # Loop through playthroughs one more time to combine any playthroughs
            # which have identical data (this could probably be done in the
            # previous loop, but eh.)
            report_stats=[pawn_stats[0]]
            for idx in range(1, len(pawn_stats)):
                cur_stats = pawn_stats[idx]
                if cur_stats == report_stats[-1]:
                    report_stats[-1].update_with_playthrough(cur_stats)
                else:
                    report_stats.append(cur_stats)

            # Now report on which ones are interesting.
            for stats in report_stats:
                if stats.is_interesting():
                    if not shown_header:
                        writer.writerow(stats.get_labels())
                        shown_header = True
                    writer.writerow(stats.get_data())
