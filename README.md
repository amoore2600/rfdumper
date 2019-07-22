# rfdumper
**Turn the Retro Freak into a cart dumping beast with this custom firmware.**

Like Rufus guiding the Wild Stallions, I am here to transform your Retro Freak in to a massively awesome cart dumping beast to legally back up your own carts. With the rfdumper firmware you can make decrypted dumps using the Retro Freak from 12 different cart types; FC, NES (\*adapter needed), SNES, SFC, Genesis/MD, TG16/PCE, GB, GBC, GBA, GG(\*adapter needed), SG100(\*adapter needed), MK3(\*adapter needed)

You can see a demo of me dumping my carts here: https://youtu.be/hB6V2Wt41kQ

The author is not liable for any damage caused by using this software / SD image etc. I do not take responsibility. Please use it at your own risk. Hopefully it won’t brick your system.

Your Retro Freak should be on Application version 2.7 before you use this custom firmware. You can see what version your device has by checking the system information on your Retro Freak. Upgrade instructions can be found on the Retro Freak web page.

**What does this firmware do for the Retro Freak?**

   This custom firmware allows for decrypted dumps of game carts to be made to the Retro Freak's SD card. The decrypted dumps are properly named using the Retro Freak's own internal database and are validated using the checksum from the database.

**Why would I want decrypted dumps of my game carts the Retro Freak already backs up my games to an SD card?**

   The backups of game carts that the Retro Freak makes without using this custom firmware are encrypted and can only be used on the Retro Freak system that made them. The reason I wanted decrypted dumps of my game carts was to audit my physical cart collection. Many of my carts are near +30 years old. I was paying hundreds of dollars for carts like Mega Man 7 and Earthbound and I wanted to know that these carts data were still good after 30 years. The Retro also Freak will warn if a carts checksum doesn't match the one in the Retro Freak's database. Having the decrypted dump also allows me to build my own checksums for me to compare the cart manually if I want.
 
   Another benefit of decrypted dumps is that the dumps are now portable and can be played on other devices with emulators or cores such as PCs, phones, flash carts, FPGAs, and even other Retro Freak systems. 
 
   I looked at many different cart dumping methods, most involved custom boutique hardware and software or DIY builds along with the paring of a computer. This made cart dumping difficult and expensive and far from future proof as operating systems and software libraries change frequently. These changes cause a lot problems for this boutique hardware. The Retro Freak is self-contained and simply writes the decrypted dumps to an SD card. SD cards and readers will likely be around in some form for the foreseeable future.  

**How do I use this custom firmware?**

   Download one of the img zip files and write it to an SD card, then just put it in the Retro Freak. If your SD card is 8GB in size, then use the 8GB image. If your SD card is 16GB in size, then use the 16GB image. If your SD card is 32GB in size, then use the 32GB image. SD cards larger than 32GB are not supported.
   
  https://github.com/amoore2600/rfdumper/raw/master/rfdumper8GB.20190720.img.zip
  
  https://github.com/amoore2600/rfdumper/raw/master/rfdumper16GB.20190720.img.zip
  
  https://github.com/amoore2600/rfdumper/raw/master/rfdumper32GB.20190720.img.zip
   
* Download the correct image file for your SD Card's size
* Unzip the file
* Write the image to the SD card, use [etcher](https://www.balena.io/etcher/), [dd](http://osxdaily.com/2018/04/18/write-image-file-sd-card-dd-command-line/) or any other image writing software
* Put a cart in the Retro Freak 
* Put the SD card in Retro Freak 
* Power on the Retro Freak
* Follow the on-screen prompts to save the cart to the SD card
* After getting the message prompt that the cart has been dumped to the SD card wait 10 to 15 seconds before hitting the close button.  
* Remove the SD card from the Retro Freak and transfer the SD card to a computer 
* Decrypted dumps will be found in the directory "/retrofd/log" on the SD card     


**So what should I know about using this custom firmware?**

   This is a slightly reconfigured version of https://github.com/hissorii/retrofd using hissorii’s excellent work. Hissorii is the reson all this is even posible. Hissorii deserves all of the credit for this custom firmware image. Hissorii, thank you so much for making your work public!!! Jonas Rosland’s awesome how to at https://gist.github.com/jonasrosland/a535f05acb8b81d6685d4d7d348b35ec also help get me up and running and building this. The credit for this dumping firmware goes to them as my changes were very minor (edits to just 1 config file and minor busybox script changes).

   It's probably best that you only use this SD card when dumping games as the dumping process can cause a lot of wear and tear on the SD card. 

**The directories on the SD card are a little bit wonky** 

   The “/RetroFreak/Games” directory on the SD card is created after you dump your first cart. The “/RetroFreak/Games” directory should always be empty. Never put files in “/RetroFreak/Games”. This custom firmware uses this directory to get the name of the game from the encrypted dump when the encrypted dumping process put it there. After the file name is retrieved files in this directory (including the encrypted dump) are removed. If multiple files are in “/RetroFreak/Games” directory, then then future decrypted dumps may be named wrong. If you see files in the “/RetroFreak/Games/” directory, you should delete them when using this custom firmware.

   You should never have a file named dump.* on the SD card in “/retrofd/log/”. This is a temporary file that's used when copying the decrypted dump. If you see files named dump.* in the “/retrofd/log/” directory you should delete them when using this custom firmware as this might cause an issue with name the decrypted dump.
      
**Be patient**

  After you get the message that the cart has been dumped wait 10 to 15 seconds before hitting the close button. This give the code time to run fully, copy the game, and rename it in the "/retrofd/log/” directory.  
