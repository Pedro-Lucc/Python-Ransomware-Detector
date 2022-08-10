import os
import time
import ransomware_check
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

rename_counter = []
counter = 0


class FileSystemModifications(FileSystemEventHandler):
    global rename_counter

    def on_created(self, event):
        print("Created: " + event.src_path)
        time.sleep(10)  # wait for the user to write the name of the file.
        ransomware_check.main()

    def on_deleted(self, event):
        print("Deleted: " + event.src_path)

    def on_modified(self, event):
        print("Modified: " + event.src_path)
        ransomware_check.main()

    def on_moved(self, event):
        print("Moved or Renamed: " + event.src_path)
        path, file = os.path.split(event.src_path)
        rename_counter.append(file)
        # One indication to know how to check Ransomware attack is when there is an increase
        # in file renames and your data becomes encrypted.
        # therefore, if we identify many of file renames, it's potential Ransomware issue.
        if len(rename_counter) > 2:
            print(f"The files {rename_counter} might be encrypted!")
        ransomware_check.main()


if __name__ == "__main__":
    paths = ['path_to_folder_or_file']
    event_handler = FileSystemModifications()
    observer = Observer()

    observers = []

    # iterate through paths and attach observers
    for line in paths:
        # convert line into string and strip newline character
        targetPath = str(line).rstrip()

        # Schedules watching of a given path
        observer.schedule(event_handler, targetPath)
        # Add observable to list of observers
        observers.append(observer)

    # start observer
    observer.start()
    try:
        while True:
            # poll every 5 second
            counter += 1
            print(f'round {counter}')
            time.sleep(5)
    except KeyboardInterrupt:
        for o in observers:
            o.unschedule_all()
            # stop observer - if interrupted.
            o.stop()
    for o in observers:
        # Wait until the thread terminates before exit.
        o.join()

if __name__ == "__main__":
    # Os caminhos que serão monitorados pelo WatchDog Observer
    paths_to_monitor = ["/home"]
    # Lista que conterá todos os Observers ativos
    observers = []

    for path in paths_to_monitor:
        Observer().schedule(FileSystemModifications, path)
        observers.append(Observer())

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        for observer in observers:
            observer.unschedule_all()
            observer.stop()
