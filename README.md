# Inverted-files-and-geo-text-search
Grid based searching :mag: 

## Inverted File and search by keywords (Part1)
Reads the data in order to create an inverted file (in memory) that can be used for query searching.

## Spatial index and spatial search (Part2)
Creates a simple spatial grid based index of the file data. The grid separates the space covered by points in 50 * 50 = 2500 equal-sized rectangles (cells), in order to create the grid you need to read the restaurant locations file and find the smallest and largest value in each coordinate (x and y). 
Then it splits the range of values in each coordinate at 50 equal value intervals.

## Spatial-text search (Part3)
A program that will read the data and create the inverted file and grid implemented in Parts 1 and 2.  

kwSpaSearchGrid function takes as a argument a query range and a list of query keywords and calculates and returns the restaurants contained
in the query range that contain all the query keywords in their tags. For that reason it uses the grid to find the restaurants contained in the query range and for
each of them verifies if it contains all the query keywords in its tags.

__Note__: A divide and conquer technique was implemented to speed up the merge-join function
