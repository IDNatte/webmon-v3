import datetime
import time

# Initialize the last minute to the current minute
last_minute = datetime.datetime.now().minute

# Initialize the file name
file_name = f"output_{last_minute}.txt"

# Open the first file for writing
with open(file_name, "w") as f:
    # Write the current minute to the file
    f.write(f"Current minute: {last_minute}\n")

    # Start an infinite loop
    while True:
        # Get the current minute
        current_minute = datetime.datetime.now().minute

        # If the minute has changed, close the current file and open a new one
        if current_minute != last_minute:
            # Close the current file
            f.close()

            # Update the last minute and file name
            last_minute = current_minute
            file_name = f"output_{last_minute}.txt"

            # Open the new file for writing
            with open(file_name, "w") as new_f:
                new_f.write(f"Current minute: {current_minute}\n")

                # Set the new file as the current file
                f = new_f

        # Write to the current file
        f.write("Data\n")

        # Sleep for 1 second before checking the minute again
        time.sleep(1)
