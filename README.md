# TM Visualizer
Python script (TMplotter.py) that takes csv files from TMdecoder (which converts binary telemetry messages from the LPC or RS41 instruments to csv files) and graphs the real-time results. Test files are located under the "TelemetryMessages" folder.

### Inputs

Requires inputs on the graphics window popup:
* Instrument type (LPC or RS41)
* filename.csv: the csv file that TM Visualizer is reading the data from
Both inputs can be selected from a dropdown menu or typed in

## Test_csv_creator

Python script that imitates the LPC instrument by creating a csv file and writing mock data to it every second. The data counts upwards and does not reflect actual expected values. Used for testing TMplotter.py
