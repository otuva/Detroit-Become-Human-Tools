# Detroit-Become-Human-Tools

sources no longer available

```
Mirror of: https://forum.xentax.com/viewtopic.php?t=19586
All credit goes to its owner. (daemon1)
```

---

```
Detroit Become Human tools. (PC, PS4)
Supports all characters with textures, skeletons and weights. Also most map objects will export.

Tool usage:

0. Change detroit.ini with your paths. On PS4 you can choose only chapters you need to extract. Base BIGFILE will have all models, chapters will mostly have map objects, but also a few characters. On PC there's only one big index file.

1. To make a list, run the tool without parameters
Example: Detroit > list.txt
It will create a list of potentially extractable game packages and their sizes (in bytes). MOST of them will have models, but there will be some with only videos, sounds or animations, these will be skipped with error message "not supported".

A list of all noticable models is included

2. To extract a package, run with 1 parameter (package code)
Example: Detroit D0F
It will make ASCII models, ASCII & SMD skeletons, just like it was before with my B2S/HR tool. ASCII format will have all UV pairs and extended info for correct bone rotations. Noesis plugin that reads them is included. For skeletal models you need to copypaste skeleton: open ascii file with model in text editor, delete 1st line ("0"), and copypaste the whole ascii skeleton there.

You can run the list created before as a batch file, it will export all packages you choose.

Half of textures will have no extension. Again, like in B2S, those must be converted to TGA with another tool (detroit_img.exe). Use a batch to convert all files in one run (included)

Beware, the tool can trigger antivirus false-positive, because they think its "suspicious".

3. To extract all animations, type "Detroit anims"
4. To extract all sounds, type "Detroit snd"
```
---

```
Animations tool. Works same on PC and PS4.

Usage:

1. run "detroit anim"
This will extract all 24500 files with anims. Sorry no progress indication, this may take a few minutes.

2. reextract models with detroit.exe (as before)
This is needed, because tool will now create "nodes" file, which is needed for animation convertion,
also it will make a new model compatible with anims tool (different axis layout, origin position shifted)

3. run "detroit_anim [anim] [nodes]"
This will extract animation, applying it to selected nodes information. Technically, any animaiton may be played with any model. If some bones are not present in the model (nodes file), animation will still be extracted, but you will see warnings, and it may not play correctly. Absolute most animations will be ok, but some are not supported, there will be errors and warnings.
```
