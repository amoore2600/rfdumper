# Retron5 save file converter

Convert Retron5 save files to and from files that can be used by the RetroPie and other emulators

## Intro

I have a bunch of cartridges from retro videogame systems like the NES, SNES, Gameboy, etc. and I was worried about losing my old save files as the 30 year old batteries powering the cartridges slowly die.

I got a Retron5 because it seemed like the least expensive machine that can read a large number of different cartridge types, and one of its little-known features is that it can copy save game data from a cartridge to an SD card and back again.

But the data is in a proprietary format, so I'm tied to the Retron5 and if it dies then I'm back to square one. 

This script will convert this proprietary format into the more common format used by other emulators such as those included with the RetroPie, and also back again to load emulator saves onto a real cartridge.

So I can back up my save files, and also swap out those dying batteries and put my save files back onto the cartridges to last another 30 years: https://www.youtube.com/watch?v=k7Xb6ucFcfU

## Requirements

This script requires Python 3, which you can find here: https://www.python.org/downloads/

If you're using a Mac, you may want to install it via homebrew: https://docs.python-guide.org/starting/install3/osx/

Someone else wrote a similar program for Windows a few years ago: https://www.retro5.net/viewtopic.php?f=5&t=257 but I have a Mac. Apparently it can run under Wine, but I wanted to write something I could run natively.

## Sample calls

Convert Retron5 save to emulator:

```
./retron5.py -i retron-saves-in/The\ Legend\ of\ Zelda\ -\ Oracle\ of\ Seasons\ \(U\)\ \[C\]\[\!\].sav -o emulator-saves-out/ -d
```

Convert emulator save to Retron5:

```
./retron5.py -i emulator-saves-in/The\ Legend\ of\ Zelda\ -\ Oracle\ of\ Seasons\ \(U\)\ \[C\]\[\!\].srm -o retron-saves-out/ -t -d
```

## Examples

### Move cartridge save to emulator

Start by creating a save on your cartridge

![Initial cartridge save](https://c2.staticflickr.com/2/1921/45299287111_69a336f85a_c_d.jpg)

Put the cartridge and an SD card into your Retron5

![Cartridge in Retron5](https://c2.staticflickr.com/2/1955/45250069522_2b4e2f235c_c_d.jpg)

Select "SD Card" for the save data location

![Use SD Card](https://c2.staticflickr.com/2/1943/31425372968_41a1a0773c_c_d.jpg)

Copy the cartridge save data to the SD card

![Copy save data to SD card](https://c2.staticflickr.com/2/1966/45250035422_a58531a58d_c_d.jpg)

Copy the save file from the SD card onto your computer, and run 

```
./retron5.py -i retron-saves-in/The\ Legend\ of\ Zelda\ -\ Oracle\ of\ Seasons\ \(U\)\ \[C\]\[\!\].sav -o emulator-saves-out/ -d
```

Copy the outputted file onto your RetroPie (or however you're running your emulator), in the same directory as your ROM file and with the same name (but the `.srm` extension)

![Copy emulator save beside ROM file](https://c2.staticflickr.com/2/1931/44386857895_14a3e60f64_c_d.jpg)

Load up the ROM on your RetroPie (other other emulator) and you'll see the same save data!

![Run your emulator](https://c2.staticflickr.com/2/1919/45250012062_9ce1b0156a_c_d.jpg)

### Move emulator save to cartridge

Now we can update our save on the RetroPie (or other emulator)

![Update emulator save](https://c2.staticflickr.com/2/1915/45249998342_ce37f99f7f_c_d.jpg)

Then copy it from the RetroPie (or other emulator) over to our computer

![Copy emulator save to computer](https://c2.staticflickr.com/2/1947/43484128090_c66b980398_z_d.jpg)

Then run

```
./retron5.py -i emulator-saves-in/The\ Legend\ of\ Zelda\ -\ Oracle\ of\ Seasons\ \(U\)\ \[C\]\[\!\].srm -o retron-saves-out/ -t -d
```

We can then copy the outputted file to our SD card and put the SD card and cartridge into the Retron5. We need to make sure the file has the name the Retron5 expects for this game, and with the `.sav` extension. You can check which name the Retron5 expects by writing out the save data from the cartridge using the steps above. 

![Cartridge in Retron5](https://c2.staticflickr.com/2/1955/45250069522_2b4e2f235c_c_d.jpg)

On the Retron5 we select to copy the save data to the cartridge

![Copy save data onto cartridge](https://c2.staticflickr.com/2/1970/43484127700_f78f39f8e3_c_d.jpg)

And now our updated save game is available on the original cartridge!

![Updated save on original cartridge](https://c2.staticflickr.com/2/1919/44577050744_96f2f364f8_c_d.jpg)

## Data format

The Retron5 save format is described here: https://www.retro5.net/viewtopic.php?f=5&t=67&start=10

And specifically the file format is:

```
typedef struct
{
   uint32_t magic;
   uint16_t fmtVer;
   uint16_t flags;
   uint32_t origSize;
   uint32_t packedSize;
   uint32_t dataOffset;
   uint32_t crc32;
   uint8_t data[0];
} t_retronDataHdr;
```

It's a header and then a bunch of compressed data, so to unpack the file we need to read past the header and then uncompress the data. There's a few values in the header, like the original size and CRC32 (checksum) of the original data, that we can use to make sure that nothing has been corrupted.
