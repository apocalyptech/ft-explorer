Data Dump Helper Scripts
========================

I ended up writing some scripts to help automate dumping info from TPS,
since pre-dumped TPS data has been historically thin on the ground.  The
general method for doing so is to execute a `getall <classtype> name` from
the console, for a big list of classes that you're interested in, and then
running an `obj dump <foo>` on the ones you don't have yet.

I'm not going to document this terribly thoroughly, but my method went
basically like this:

1. Jump into a level I'm interested in
2. From the console, `exec names` *(see the "`names`" file -- this is what
   executes that big ol' list of `getall` commands)*
3. Quit the game so the log gets flushed
4. Run `gen_obj_dump_list.py`, which reads in `launch.log`.  This'll output
   one or more `objectN` files, starting with `object1`, which contain `obj
   dump` statements for objects we haven't seen yet.  The file
   `found.json.xz` is used to keep track of which ones we've seen.  The
   engine seems to crash if it sees somewhere over 60k `obj dump` commands
   all at once, hence splitting the files up.
5. Start the game again, jump back into that level.
6. From the console, `exec object1` *(and so on, if there are more files)*
7. *(I tend to hop to the next map in the list at this point, before
   quitting, and `exec names` there)*
8. Quit the game so the log gets flushed
9. Run `categorize_data.py` to read `launch.log` and actually dump the
   relevant data into the relevant files.
10. If I've already done an `exec names` on a new map, run
    `gen_obj_dump_list.py` to generate a new set of `obj dump` commands,
    rinse, repeat.

A bit hokey, but it worked out quite well.  Once I was done with all the
levels, I also went through a couple more iterations of loading games with
various characters, so I was sure to get character-specific objects as
well.
