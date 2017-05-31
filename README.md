## Gem Spy

A Sublime Text plugin used to facilitate working with Ruby projects using Bundler. Inspired by the [Sublime Gem Browser](https://github.com/NaN1488/sublime-gem-browser), but re-written from scratch.

This plugin allows you to open the source for a Gem installed for the current project as well as restore the gems to their "pristine" un-edidted state. This is helpful if you need to quickly read the source for the exact version of a Gem you are running or want to be able to debug Gem related issues you might be seeing.

Currently only works with rbenv, but if I have time I'll add rvm support.

## Installation

## Usage

Open the Command Pallete with `ctrl-shift-p` or `cmd-shift-p` (depending on your platform). Type in `Gem Spy` and you will be given the following options:

- `Gem Spy: Open Gem in New Window` - opens the source for a gem in a new Sublime Text window
- `Gem Spy: Open Gem in Current Window` - opens the source for a gem in your current Sublime Text window
- `Gem Spy: Restore a Gem to Pristine State` - runs the equivalent of `gem pristine` on a gem, un-doing any local changes you might have made
- `Gem Spy: Restore all Gems to a Pristine State` - undoes all local gem changes for the current project
- `Gem Spy: Clear Cache` - clears the Gem Spy cache. Might be useful if you're experiencing bugs.

## Configuration

You can view the default settings by opening the command pallete and selecting `Preferences: Gem Spy - Default`. If you want to customize any settings, select `Preferences: Gem Spy - User` instead and make the changes in that file.

The current available preferences are:

- `sublime_path`: The path to your CLI sublime executable. This must be set in order for the plugin to work. This may be changed in a future release to be dynamically retrieved.

## Future Plans / TODO

- Add RVM support
- Test with other OS's
- Expand the README
- Actually check the output of the bundle commands to detect errors
- Create a local fork of a gem and point your bundler config to it (maybe)
