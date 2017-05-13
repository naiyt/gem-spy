import os
import json
import re
import os.path
import filecmp
import pipes
import fnmatch
import subprocess
import sublime
import sublime_plugin
import tempfile
import hashlib
from shutil import copyfile

class SpyOnGemsCommand(sublime_plugin.WindowCommand):
    def __init__(self, window):
        self.settings = sublime.load_settings('gem-spy.sublime-settings')
        self.gems = []

        super(SpyOnGemsCommand, self).__init__(window)


    #
    #
    # Lifecycle

    def run(self, **kwargs):
        self.opts = kwargs
        self.gems = self.get_gems()
        self.window.show_quick_panel(self.gems, self.on_selected)

    def on_selected(self, selected):
        if selected != -1:
            gem_name = re.search('(.*)\(', self.gems[selected]).group(1)
            gem_path = self.run_bundle_command("show " + gem_name)
            open_option = '-a' if self.opts['add_to_current_window'] else '-n'
            self.open_in_sublime([open_option, gem_path.rstrip()])



    #
    #
    # Gem fetching and caching

    def get_gems(self):
        project_name = self.window.folders()[0].split('/')[-1]
        cache_file_path = '/'.join([self.cache_directory(), project_name + "_gemfile.cache"])
        gemfile_lock_path = self.window.folders()[0] + "/Gemfile.lock"

        gems_list = []

        try:
            with open(cache_file_path, 'r') as cache_file:
                cache_json = json.load(cache_file)
        except FileNotFoundError:
            cache_json = None

        gemfile_lock_md5 = str(self.md5(gemfile_lock_path))
        if self.cache_is_valid(cache_json, gemfile_lock_md5):
            gems_list = cache_json['gems']
        else:
            output = self.run_bundle_command('list')
            gems = str(output, encoding = 'utf-8')

            for gem in gems.split('\n'):
                gem_name = re.search('\* (.*)', gem)
                if gem_name:
                    gems_list.append(gem_name.group(1))

            cache   = { 'md5': gemfile_lock_md5, 'gems': gems_list }
            with open(cache_file_path, 'w') as cache_file:
                json.dump(cache, cache_file)

        return gems_list

    def cache_is_valid(self, cache_json, gemfile_lock_md5):
        valid_cache = cache_json and cache_json['md5'] == gemfile_lock_md5
        log_message = "cache hit" if valid_cache else "cache miss"
        self.log(log_message)
        return valid_cache

    def cache_directory(self):
        sublime_cache = sublime.cache_path()
        cache_path = sublime_cache + "/gem-spy"

        if not os.path.exists(cache_path):
            os.makedirs(cache_path)

        return cache_path

    # http://stackoverflow.com/a/3431838/1026980
    def md5(self, fname):
        hash_md5 = hashlib.md5()
        with open(fname, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()



    #
    #
    # Utilities

    def run_bundle_command(self, command):
        current_path = self.window.folders()[0]
        rbenv_command = os.path.expanduser('~/.rbenv/shims/bundle ' + command)
        process = subprocess.Popen(rbenv_command.split(), cwd=current_path, stdout=subprocess.PIPE)
        output = process.communicate()[0]
        return output

    def open_in_sublime(self, args):
        args.insert(0, self.settings.get('sublime_path'))
        subprocess.Popen(args)

    def log(self, message):
        if self.settings.get('debug'):
            print("Gem Spy Logger: " + message)