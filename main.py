import csv
import math








def main():

    currentHeight = None #setting a curent height which changes if more than 1 file is read.
    output_data = []

    with open('input.csv', newline='') as input:
        inputFile = csv.reader(input)

        for line in inputFile:

            timestamp = line[0]
            seconds = timestamp[-3:-1].strip()
            
            if  line[1].strip().isnumeric():
                height =  int(line[1].strip())

            if currentHeight is None:
                currentHeight = height #setting up the height to be built up
                output_data.append([timestamp, currentHeight])
                continue

            
            #calculating movement
            if height != currentHeight:
                heightDiff = abs(height - currentHeight)
                timeNeeded = heightDiff
                
                
                startTimeMinutes = 60 - (timeNeeded // 2)
                endTimeMinutes = (timeNeeded // 2)

                startHour = int(timestamp[11:13]) -1
                startTimeStamp = f"{timestamp[:11]}{startHour:02}:{startTimeMinutes:02}:{seconds}Z"

                endHour = (startHour + 1) % 24
                endTimeStamp = f"{timestamp[:11]}{endHour:02}:{endTimeMinutes:02}:{seconds}Z"

                output_data.append([startTimeStamp, currentHeight])
                output_data.append([endTimeStamp, height])

                currentHeight = height
            
    with open('output.csv', 'w', newline='') as output:
        outputWriter = csv.writer(output)        
        outputWriter.writerows(output_data)
           






if __name__ == "__main__":
    main()