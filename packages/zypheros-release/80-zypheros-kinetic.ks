# ZypherOS Kinetic: run by Anaconda after installing. Clears a blsdir left
# in the GRUB environment by an image built on a btrfs host; without it the
# installed system boots to an empty GRUB menu.
%post
grub2-editenv - unset blsdir
%end
