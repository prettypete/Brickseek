# Brickseek
Unofficial Brickseek API for product inventory checking 

# Inspiration 
theriley106 had a wonderful API that no longer works, so I updated it to use Selenium as Brickseek runs dynamic JS

# Installation 
Clone this repo and install dependencies. It's set-up to do so in any venv 

# Usage 
    ## Checks for JBL headphones near 02139 in Walmart and Target and outputs json to headphones.txt
    python brickseek.py -u 050036332392 -z 02139 -s a -o headphones
    ## Provides a guide on how to run the script
    python brickseek.py -h 
    
# Stores 
Currently, the Brickseek API works with 
	Target
	Walmart
	Lowes
	Office Depot
	Staples

More stores can be integrated

Note: This API, like Brickseek, should NOT be used in stores to prove stock availability, quantity and/or price.
