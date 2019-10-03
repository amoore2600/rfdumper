# rfdumper
**Turn the Retro Freak into a cart dumping beast with this custom firmware and configuration**

Like Rufus guiding the Wild Stallions, I am here to transform your Retro Freak in to a massively awesome cart dumping beast to legally back up your own carts. With the rfdumper firmware you can make decrypted dumps using the Retro Freak from 12 different cart types; FC, NES (\*adapter needed), SNES, SFC, Genesis/MD, TG16/PCE, GB, GBC, GBA, GG(\*adapter needed), SG100(\*adapter needed), MK3(\*adapter needed)

You can see a demo of me dumping my carts here: https://youtu.be/HHIULSM6eyw

Demo of dumping SRAM (save progress from cart): https://youtu.be/uAxWo9JGH2M

*The author is not liable for any damage caused by using this software / SD image etc. I do not take responsibility. Please use it at your own risk. Hopefully it won’t brick your system.*

Using this this custom firmware proprley will not make changes to your Retro Freak. This firmware is contained to the SD card. Remove the SD card at any time to return the Retro Freak to its normal state.  

Your Retro Freak should be on application version 2.7 before you use this custom firmware. You can see what version your device has by checking the system information on your Retro Freak. Upgrade instructions can be found on the Retro Freak web page.

YOU SHOULD READ THIS DOCUMENT IN IT'S ENTIRETY SO YOU UNDERSTAND HOW THIS ALL WORKS!!!!!

**What does this firmware do for the Retro Freak?**

   This custom firmware allows for decrypted dumps of game carts to be made to the Retro Freak's SD card including SRAM (game save). The decrypted dumps are properly named using the Retro Freak's own internal database and are validated using the checksum from the database.

**Why would I want decrypted dumps of my game carts the Retro Freak already backs up my games to an SD card?**

   The backups of game carts that the Retro Freak makes without using this custom firmware are encrypted and can only be used on the Retro Freak system that made them. The reason I wanted decrypted dumps of my game carts was to audit my physical cart collection. Many of my carts are near +30 years old. I was paying hundreds of dollars for carts like Mega Man 7 and Earthbound and I wanted to know that these carts data were still good after 30 years. The Retro Freak will also warn if a cart's checksum doesn't match the one in the Retro Freak's database during the dumping process meaning the cart could be corrupt or the carts checksum is not in the database. Having the decrypted dump also allows me to build my own checksums for me to compare the cart manually if I want.
 
   Another benefit of decrypted dumps is that the dumps are now portable and can be played on other devices with emulators or cores such as PCs, phones, flash carts, FPGAs, and even other Retro Freak systems. 
 
   I looked at many different cart dumping methods, most involved custom boutique hardware and software or DIY builds along with the paring of a computer. This made cart dumping difficult and expensive and far from future proof as operating systems and software libraries change frequently. These changes cause a lot of problems for this boutique hardware. The Retro Freak is self-contained and simply writes the decrypted dumps to an SD card. SD cards and readers will likely be around in some form for the foreseeable future.  

**How do I use this custom firmware?**

Download one of the img zip files from here: 
   
   https://github.com/hissorii/retrofd/releases/download/v1.0/retrofd_v1.0_8GB.zip
   
   https://github.com/hissorii/retrofd/releases/download/v1.0/retrofd_v1.0_16GB.zip
   
   https://github.com/hissorii/retrofd/releases/download/v1.0/retrofd_v1.0_32GB.zip
   
If your SD card is 8GB in size, then use the 8GB image. If your SD card is 16GB in size, then use the 16GB image. If your SD card is 32GB in size, then use the 32GB image. SD cards larger than 32GB are not supported. Then unzip and write the .img file to an SD card with dd or etcher or any other image writing software.  Copy the text if the these 2 files below and place them in the largest partition on the SD card in the "/retrofd" directory overwriting the 2 files that already exist (retrofd.cfg and rfd_logcd.sh).
   
Copy the code below to a file and name this file rfd_logcd.sh. Place this file in the largest partition on the SD card in the "/retrofd" directory overwriting the file that already exist. 

```busybox
#!/sbin/busybox sh

while ! busybox grep "/mnt/external_sd" /proc/mounts > /dev/null
do
	busybox sleep 1
done

srcd=/mnt/ram/
dstd=/mnt/external_sd/dumps
busybox rm $dstd/dump.* 
busybox rm /mnt/external_sd/RetroFreak/Games/* 
busybox rm -rf /mnt/external_sd/RetroFreak/Saves/* 
busybox mkdir -p /mnt/external_sd/sram/
busybox mkdir -p /mnt/external_sd/dumps/

# copy log files(/mnt/ram/log/*) to SD(/retrofd/log) if new ones exist
while : ;
do
	busybox find $srcd -maxdepth 1 -type f | busybox sed -e 's/.*\///' | while read logfile
	do
		[ -f "$dstd/$logfile" ] || busybox sleep 5 && busybox cp "$srcd/$logfile" "$dstd/${eromdump}"  
	done
	                   # copy SRAM remove first 24 bits from file and decompress SRAM. crc232 is in bits 16-24 not checked with this code.
                            eromdump=`busybox ls /mnt/external_sd/RetroFreak/Games/`
                            fnesramdump="`busybox find "/mnt/external_sd/RetroFreak/Saves/" -name *.sav | busybox awk -F "/" '{print$8}'`"
                            if [ ! -z "${fnesramdump}" ]
                               then
                                  esramdump=`busybox find /mnt/external_sd/RetroFreak/Saves/ -name *.sav`
    				  busybox tail -c +25 "${esramdump}" > /mnt/external_sd/sram/out.sav-24
                                  busybox printf "\x1f\x8b\x08\x00\x00\x00\x00\x00" | busybox cat - /mnt/external_sd/sram/out.sav-24 | busybox gzip -dc >  "/mnt/external_sd/sram/${fnesramdump}"
                                  busybox rm -rf /mnt/external_sd/RetroFreak/Saves/*
                                  busybox rm /mnt/external_sd/sram/out.sav-24
                            fi
                            busybox rm /mnt/external_sd/RetroFreak/Games/*
                            busybox rm $dstd/dump.* 
	busybox sleep 1
done

```


Copy the code below to a file and name this file retrofd.cfg. Place this file in the largest partition on the SD card in the "/retrofd" directory overwriting the file that already exist. 

```
# clear micro SD partition 2/3
RF_CLR_SDP23=no
# FACTORY TEST MODE
RF_FTM=no
# Log copy daemon
RF_LOGCD=yes

```

Here is an example ofthe directory and file layout for SD CARD on the Largest Partition, if your using Windows this is the only partions avalible on the SD card.

```

├── retrofd
│   ├── bootscript.sh
│   ├── install_apk
│   ├── install_done
│   ├── inst_apk.sh
│   ├── local.prop
│   ├── local.prop.adb
│   ├── local.prop.adb_rooted
│   ├── local.prop.noline
│   ├── log
│   ├── mk_rfd_img.sh
│   ├── retrofd.cfg <---Overwrite this file with examples above.
│   ├── retrofd.sh
│   ├── rfd_clr_done
│   ├── rfd_logcd.sh <---Overwrite this file with examples above.
│   └── rfgui_no_ftm
└──────────────────────────
```
Step by step info for getting started:
   
* Download the correct image file for your SD Card's size
* Unzip the file
* Write the image to the SD card, use [etcher](https://www.balena.io/etcher/), [dd](http://osxdaily.com/2018/04/18/write-image-file-sd-card-dd-command-line/) or any other image writing software
* Add the 2 files above to the SD card on the largest partition in the "/retrofd" directory overwriting the 2 existing files (This will be the only partition Windows users can see)
* Put the SD card in Retro Freak
* Power on the Retro Freak without a cart in it
* Set the "Save data location" to "microSD card" in the "System Menu" (this only needs to be done once)
* Power off the Retro Freak 
* Put a cart in the Retro Freak 
* Power on the Retro Freak
* Follow the on-screen prompts to dump the cart and sram to the SD card
* After getting the message prompt that the cart has been dumped to the SD card BE PATIENT wait 10 to 15 seconds before hitting the "close" button  
* Remove the SD card from the Retro Freak and transfer the SD card to a computer 
* Decrypted dumps will be found on the largest partition in the "/dumps" directory on the SD card and will be properly named
* Decrypted SRAM dumps (saves) will be found in the "/sram" directory
* Do not use this SD Card with custom firmware and configuration to play dumps or carts. Only use it for dumping carts. Transfer your dumps and SRAM files to another SD card for every day play.
* When you done dumping carts, power down the Retro Freak, remove this SD Card from your Reto Freak and restart your system. The Retro Freak will return to its normal state. 

The dumping process can cause a lot of wear and tear on the SD Card. This firmware and configuration will dump a cart even if the cart has been previously dumped to the SD Card. 

**Be patient**

  After you get the message that the cart has been dumped wait 10 to 15 seconds before hitting the close button. This gives the code time to run fully, copy the game, and rename it in the "/dumps” directory.  

**This custom firmware with this configurations should not be used to play dumps or carts!!!!**

Do not use this SD Card with custom firmware and configuration for every day play. Only use it for dumping carts. Transfer your dumps including SRAM (saves) to another SD card for every day play. You will likely see and errors if you play a cart and try to save your progress to it using this custom firmware and configuration. (You have been warned!)  

USE CAUTION - This SD Card with custom firmware and configuration it will not save your SRAM (save) game progress if you use it to play games. This SD Card with custom firmware and configuration should only be used for dumping carts. (You have been warned!)  

USE CAUTION - This SD Card with custom firmware and configuration dumps the cart and SRAM every time the Retro Freak is powered on with a cart and this SD Card. This will overwrite the existing dump from the cart on to the SD Card including the SRAM file on the SD card.

This SD Card with custom firmware and configuration does not save your dumps where the Retro Freak expects. The dumps and SRAM files can not be managed using the Retro Freak's built in file browser.   

**So what should I know about using this custom firmware?**

   This is a slightly reconfigured version of https://github.com/hissorii/retrofd using Hissorii’s excellent work. Hissorii is the reason all this is even possible. Hissorii deserves all of the credit for this custom firmware image. Hissorii, thank you so much for making your work public!!! Jonas Rosland’s awesome how to at https://gist.github.com/jonasrosland/a535f05acb8b81d6685d4d7d348b35ec helped get me up and running and building rfdumper. The credit for this dumping firmware goes to Hissorii and Jonas Rosland as my changes were very minor (edits to just 1 config file and minor busybox script changes).


**The directories on the SD card are a little bit wonky.** 

In the largest partition on the SD Card: 

   The "/retrofd" directory is where all of the bits needed to run the firmware, be careful dragons live here, it's best to leave this alone unless you know what your doing.

   The “/RetroFreak/Games” and “/RetroFreak/Saves/SRAM/\<SYSTEM>/” directories on the SD card are created after you dump your first cart and dump your first SRAM save file. The “/RetroFreak/Games” and “/RetroFreak/Saves/SRAM/\<SYSTEM>/” directories should always be empty. Never put files in “/RetroFreak/Games” or “/RetroFreak/Saves/SRAM/\<SYSTEM>/”. This SD Card with custom firmware uses these directories to get the name of the game from the encrypted dump and or SRAM save file when the encrypted dumping process puts it there. After the filename is retrieved files in these directories any files in them are removed. If any files are in “/RetroFreak/Games” or “/RetroFreak/Saves/SRAM/\<SYSTEM>/” directory, then future decrypted dumps and SRAM save files may be named wrong. If you see files in the “/RetroFreak/Games/” or “/RetroFreak/Saves/SRAM/\<SYSTEM>/” directories, you should delete them when using this custom firmware.

The directories "/dumps" and "/sram" are created after dumping your first cart. You should never have a file named dump.* on the SD card in “/dumps”. This is a temporary file that's used when copying the decrypted dump. If you see files named dump.* in the “/dumps” directory you should delete them when using this custom firmware as this might cause an issue with name the decrypted dump.
   
**My dump is named "UnknownGame_??????????"**

If the cart that you dumped has a name similar to "UnknownGame_F36FFEE1.PCE" don't panic. This means that the Retro Freak does not have this game in its database. The letters and numbers in the dump’s file name are the CRC32 checksum for the dump "F36FFEE1". You can use this string to look up the game online. In the case of ["UnknownGame_F36FFEE1.PCE"](https://www.google.com/search?q=F36FFEE1) this is the lesser known version for the USA/Europe cart for Bonk's Revenge. see a demo of this example here: https://youtu.be/Xv3k6jRHRU0You 

You can also try searching the rdfumper-checksum.txt to see if the checksum can be found there. (use your browser serch/find comand, "Ctrl"+ F): https://raw.githubusercontent.com/amoore2600/rfdumper/master/rfdumper-checksum.txt

It's also likely if your cart is a homebrew, hack, prototype, beta or unlicensed cart that your cart won't be in the Retro Freaks database. Use the CRC32 checksum to look for the game online.

Another reason sometimes carts are not recognized is that the pins are dirty. Try cleaning them with some isopropyl alcohol and some q tips.

The last reason for a dump being unknown is that cart is damaged or corrupt. It’s unfortunate but sometimes these games just go bad and there’s not much you can do to repair it short of changing out the eproms or failing components. 

**Transfering SRAM game save files back to a real cart**

rfdumper already dumps decrypted SRAM files to the "/sram" directory on the SD card. These SRAM save files can be used in emulators, flash carts, FPGAs, ect to transfer your progress. However, you can also take SRAM files from these devices and use the Retro Freak to re-write these files to a real cart. The SRAM file needs to be converted to a file that the Retro Freak can use. You can use the utilities here to convert the SRAM save files, these tools work for both the Retro Freak and Retron 5:

https://github.com/amoore2600/rfdumper/tree/master/SRAM-Utilites

You should also use a different SD card than the one you use for the rfdumper firmware to transfer the SRAM save file back to the cart!!!

You can see a demo of how to convert SRAM save files here for Linux but the process is similar for Windows too.

https://youtu.be/xLW5heS8WR8
