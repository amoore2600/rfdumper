# rfdumper
Turn the Retro Freak into a cart dumping beast with this custom firmware.

Like Ruffus guiding the Wild Stallions, I am here to transform your Retro Freak in to a massively awesome cart dumping beast.

*What does this firmware do for the Retro Freak?*

  This custom firmware allows for decrypted dumps of game carts to be made to the Retro Freak's SD card. The decrypted dumps are properly named using the Retro Freak's own internal database and are validated using the checksum from the database.

*Why would I want decrypted dumps of my game carts the Retro Freak already backs up my games to an SD card?

  The back ups of game carts that the Retro Freak makes without using this custom firmware are encrypted. The reason I wanted decrypted dumps of my game carts was to audit my physical cart collection. Many of my carts are near +30 years old. I was paying hundreds of  dollars for carts like Megaman 7 and Earthbound and I wanted to know that these carts data were still good after 30 years. The Retro also Freak will warn if a carts checksum doesn't match the Retro Freak's database and having the decrypted dump also allows me to build my own checksums for me to compare manually if I want.
 
 Another benefit of decrypted dumps is that the dumps are now portable and played on other devices such as PCs, flash carts, FPGAs, and even other Retro Freak systems. 
 
 I looked at many different cart dumping methods, most involved custom boutique hardware and software or DIY builds along with paring of a computer. This made cart dumping difficult and expensive and far from future proof as operating systems and libraries change frequently and then causes problems for these boutique systems. The Retro Freak is self contained and simply writes the decrypted dumps to an SD card which will likely be around in some form for the foreseeable future.  Also the Retro Freak can dump 11 different cart formats.  

*How do I use this custom firmware?

  Download one of the img zip files and write it to an SD card then just put it in the Retro Freak. If your SD card is 8GB in size then use the 8GB image. If your SD card is 16GB in size then use the 16GB image. If your SD card is 32GB in size then use the 32GB image.

Unzip the image 
Write the image to the SD card (use dd, etcher, or any other image writing software)
Put a cart in the Retro Freak 
Put the SD card in Retro Freak 
Power on the Retro Freak
Follow the on screen prompts to save the cart to the SD card
Remove the SD card from the Retro Freak and transfer the SD card to a computer 
Decrypted dumps will be found in /retrofit/log on the SD card     


*So what should I know about using this custom firmware?

  The author is not liable for any damage caused by using this software / SD image etc. I do not take responsibility. Please use it at your own risk.

  This is a repackaged version of https://github.com/hissorii/retrofd using hissorii’s excellent work! Also this would not be possible with Jonas Rosland’s awesome how to at https://gist.github.com/jonasrosland/a535f05acb8b81d6685d4d7d348b35ec The credit for this dumping firmware goes to them as my changes were very minor.

  It's probably best that you only use this SD card when dumping games as the dumping process can cause a lot of wear and tear on the SD card. 

*The directories on the SD card are a little bit wonky. 

  The “/RetroFreak/Games” directory on the SD card should always be empty never put files in it. This custom firmware uses this directory to grab the name of the game from the encrypted dump when the dumping process put it there. If multiple files are in this directory then the  decrypted dump my be named wrong. If you see files in the “/RetroFreak/Games/” directory you should delete them when using this custom firmware.

  You should never have a file named dump.* on the SD card in “/retrofd/log/”. This is a temporary file that's used when copying the decrypted dump. If you see files named dump.* in the “/retrofd/log/” directory you should delete them when using this custom firmware.
