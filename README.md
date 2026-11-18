## Disclaimer

This project is provided "AS IS", without warranty of any kind, express or
implied, including but not limited to the warranties of merchantability,
fitness for a particular purpose, and non-infringement.

Modifying and flashing device firmware is risky and can permanently damage
("brick") your tablet, void its warranty, or cause it to behave unexpectedly.
You use this project entirely at your own risk. In no event shall the authors
or contributors be liable for any claim, damages, or other liability, whether
in an action of contract, tort, or otherwise, arising from, out of, or in
connection with this project or its use, including damage to your device or
data.

This is an independent, unofficial project. It is not affiliated with,
endorsed by, or supported by Huion or GigaDevice. "Huion", "Inspiroy" and
"GD32" are trademarks of their respective owners.

Always make and verify a full backup before flashing, and keep a copy of your
original firmware.

# Huion Inspiroy H430P: back up, patch and flash the app firmware (no smoothing filter)

Tool: GD32 DFU Tool (GigaDevice) on Windows. Chip: GD32F350G8U6.

> **Warning.** Flashing can brick the tablet. Make and verify a backup first. Always flash at **`0x08004000`**, never `0x08000000`, and never tick "Erase All".

## 0. What you are dealing with

Flash layout (confirmed from a full 64 KB dump):

| Range | Pages | Contents |
|---|---|---|
| `0x08000000`-`0x08003363` | 0-12 | Bootloader (DFU / app launcher) |
| `0x08003364`-`0x08003FFF` | 12-15 | Blank (`0xFF`) |
| `0x08004000`-`0x0800BFFF` | **16-47** | **Application firmware (32 KB). This is what you back up and flash.** |
| `0x0800C000`-`0x0800FFFF` | 48-63 | Blank (`0xFF`) |

The 32 KB `.bin` files are the **application only**, built to run at `0x08004000`. Always flash them at `0x08004000`.

## 1. Files

| File | Purpose |
|---|---|
| `huion_backup_original.bin` | Original stock app (32,768 bytes). SHA-256 `72f12d7dbfea82679dce90fcd5d1207172ed7efad43f0fcedaceabad54e6a12a` |
| `huion_backup_nofilter.bin` | Stock app with the smoothing filter bypassed. SHA-256 `1c107d9a6ec95deef9420b806f57fbd458a573c3230da07502850e780ad7bb54` |
| `huion_nofilter.ips` | The same change as an IPS patch. SHA-256 `27aa74bbcbecc7be3ee4eddd3ce307df389bf7940b670582f518f66bdbfebf9a` |
| `GD32_Dfu_Tool_V3.8.2.9056.rar` | GD32 DFU Tool. SHA-256 `07D1ED17C3C1F6EDD9BBE6774F424DE36D8D61055289622E40392C5530C6A575` |
| `GD32DfuDrivers_V3.6.6.6167.rar` | GD32 DFU drivers. SHA-256 `65760A54259CE278C98630F3F6C4BB0A2EC9D829BE3CC1A3F5D60CA1C8C42D16` |

## 2. What the patch does

One 2-byte change at file offset `0x3316`: `70 48` becomes `C0 E0`. This skips the pen smoothing block (adaptive weighted averaging plus a jitter dead-zone). Everything else is stock.

## 3. Put the tablet in DFU mode

The tool should list **GD DFU DEVICE 1** and show Flash 64 KB, VID 0x28E9, PID 0x0189. Hold the top right button while plugging the cable to enter DFU mode. Install the GD32 DFU drivers first if the device isn't recognized.

## 4. Back up the app (do this first)

1. Select **Upload from Device**.
2. Click **open** next to "UL APP file name" and choose a save path, e.g. `app_backup.bin`.
3. Click **OK**. In **Select Pages**, tick **pages 16 to 47** only (Page16 starts at `0x8004000`, Page47 ends at `0x800BFFF`).
4. Click **OK** and wait for 100%.
5. Verify: the file must be exactly 32,768 bytes. Repeat the upload once and compare the SHA-256 of both.

Keep the original stock backup and this verified copy somewhere safe.

## 5. Create the patched file

Use the ready-made `huion_backup_nofilter.bin`, or build it yourself using an IPS patcher or the included `patcher.py` (run it in the same folder as `huion_backup_original.bin`; it writes `huion_backup_nofilter.bin`).

Then check the SHA-256 of the result against the table above before flashing.

## 6. Flash

1. Enter DFU mode and select the device.
2. Select **Download to Device**.
3. Click **open** next to "DL APP file name" and choose the 32 KB `.bin`.
4. Set **@0x** to **`8004000`**.
5. Tick **Verify after download**. Leave **Erase All** unticked.
6. Click **OK** and wait for completion.
7. Click **Leave DFU** to reboot.

**Verify the flash:** re-enter DFU mode, upload pages 16 to 47 again, and compare the SHA-256 of the result to the file you flashed. They must match exactly.

## 7. Restore stock

Repeat section 6 with `huion_backup_original.bin` (or your verified `app_backup.bin`) at `8004000`.

## 8. Troubleshooting

- **Pen jitters when held still.** Expected: the jitter dead-zone is part of the removed block. Restore stock, or use OTD filters.
- **Tablet doesn't boot after flashing.** Re-enter DFU mode and reflash the stock file at `8004000`. If DFU mode is unreachable, well, you have been warned.
