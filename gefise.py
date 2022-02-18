import os
import re
import subprocess
import yaml

def readConf():
    with open("efi-entries.yml", "r") as stream:
        try:
            entry_dict = yaml.safe_load(stream)
            return entry_dict
        except yaml.YAMLError as exc:
            print(exc)

def fetchEntryIndex(label, entry_array):
    for entry in entry_array[3:]:
        index = re.search("\d{4}(?=\* " + label + "$)", entry)
        if index != None:
            return str(index.group())
    return None

def addEntries(entries):
    cur_entries = subprocess.run(['efibootmgr'], stdout=subprocess.PIPE)
    cur_entries_array = cur_entries.stdout.decode().split('\n')
    added_entries = [None] * len(entries.items())
    for label, entry in entries.items():
        pri = entry['priority']
        disk = entry['disk']
        part = entry['partition']
        loader = entry['loader']
        root = entry['root']
        initrds = entry['initrd']
        params = entry['params']
        full_params = ""
        if root:
            full_params += "root=" + root + " "
        if initrds:
            for image in initrds:
                full_params += "initrd=" + image + " "
        if params:
            for param in params:
                full_params += param + " "
        flags = ["efibootmgr", "--disk", disk, "--part", str(part), "--create", "--label", label, "--loader", loader]
        if full_params != "":
            flags.extend(["--unicode", full_params.strip()])
        cur_entry_index = fetchEntryIndex(label, cur_entries_array)
        if cur_entry_index != None:
            delete_entry = subprocess.run(['efibootmgr', '--bootnum', cur_entry_index, '--delete-bootnum'], stdout=subprocess.PIPE)
        print(flags)
        new_entries = subprocess.run(flags, stdout=subprocess.PIPE)
        new_entries_array = new_entries.stdout.decode().split('\n')
        new_entry_index = fetchEntryIndex(label, new_entries_array)
        if new_entry_index == None:
            new_entry_index = "0000"
        pri_index = pri - 1
        added_entries[pri_index] = new_entry_index
    return added_entries

def main():
    entries = readConf()
    priority_array = addEntries(entries)
    os.system('efibootmgr --bootorder ' + ','.join(priority_array))

if __name__ == "__main__":
    main()
