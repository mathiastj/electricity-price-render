#!/usr/bin/env python

# import library for fetching Elspot data
from nordpool import elspot
from pprint import pprint
import matplotlib.pyplot as plt
from matplotlib.ticker import StrMethodFormatter
import sys

# define when power is considered expensive
# to always have the same reference in the chart
expensive = 0.5

# convert to dkk/kwh, add danish VAT of 25%, and round to 2 decimals. Price is in dkk/mWh
def normalize(price):
    return round(price*1.25/1000, 2)

# initialize class for fetching Elspot prices in DKK
prices_spot = elspot.Prices(currency='DKK')

# get the prices per hour for the eastern part of Denmark
# the price at position 0 matches 00:00-01:00 in the Copenhagen timezone
hourlyEastDenmarkPrices = prices_spot.hourly(areas=['DK2'])

# get the date from the end field, it is in utc so end is 22 or 23 in Copenhagen
date = hourlyEastDenmarkPrices.get('end', {})
# format date in standard Danish notation
formattedDate = date.strftime('%d/%m/%y')
fileFormattedDate = date.strftime('%Y-%m-%d')

priceValues = hourlyEastDenmarkPrices.get('areas',{}).get('DK2', {}).get('values', {})

# exit if there is no data
if len(priceValues) == 0:
    sys.exit(0)

# exit if price values are infinity (just check the first), this means they are not set for the day yet
if priceValues[0]['value'] == float('inf'):
    sys.exit(0)

# get the average
average = normalize(hourlyEastDenmarkPrices.get('areas',{}).get('DK2', {}).get('Average',{}))

# normalize the prices
normalizedPrices = [normalize(i['value']) for i in priceValues]

# Create hours for x axis from 0-23
hours = [x for x in range(24)]

# create bar chart
plt.bar(hours,normalizedPrices)
# add labels
plt.xlabel('hour')
plt.ylabel('DKK/kWh')
# add date as title
plt.title(formattedDate)
# set ticks
plt.xticks([0,4,8,12,16,20,23])
# add the average as a line
plt.axhline(y=average, linewidth=1, linestyle='--')
# add the expensive point of electricity as a line
plt.axhline(y=expensive, linewidth=1, linestyle='--', color='r')
# force two decimals on y axis
plt.gca().yaxis.set_major_formatter(StrMethodFormatter('{x:,.2f}'))
# tighten x limits around the hours
plt.xlim(xmin=-0.5,xmax=23.5)
# get borders
x0,x1 = plt.gca().get_xlim()
# add average text to average
plt.text(x1+0.1, average, 'average')
# add expensive text to expensive
plt.text(x1+0.1, expensive, 'expensive').set_fontsize(8)
# save the plot as file
plt.savefig('daily_prices/' + fileFormattedDate + '.png', dpi=200)
