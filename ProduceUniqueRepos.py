import pandas as pd
import os
import zipfile

# unzip the CSV file
with zipfile.ZipFile('sonar_measures.zip', 'r') as zip_ref:
    zip_ref.extractall('./')

# Load the CSV file
df = pd.read_csv('sonar_measures.csv', low_memory=False)

# Get the unique project names for further use in link logic
unique_projects = df['project'].unique()

# Base URL for Apache's GitHub repositories
base_url = "https://github.com/apache/"

output = ''

# Add the missing links manually
missing_links = [
    "https://github.com/apache/jspwiki",
    "https://github.com/apache/poi",
    "https://github.com/apache/pdfbox-jbig2",
    "https://github.com/apache/dolphinscheduler",
    "https://github.com/apache/ratis",
    "https://github.com/apache/daffodil",
    "https://github.com/apache/incubator-nemo",
    "https://github.com/apache/roller",
    "https://github.com/apache/knox",
    "https://github.com/apache/ant",
    "https://github.com/apache/logging-log4cxx"
]

# Print each project as a link
for project in unique_projects:
    
# Remove "apache_" prefix because it is a part of the base_url
    if project.startswith("apache_"):
        formatted_project = project[7:]  # Remove the first 7 characters
    else:
        formatted_project = project

    # Replace underscores with hyphens for the URL because of the link logic in use
    formatted_project = formatted_project.replace('_', '-')
    link = f"{base_url}{formatted_project}"
    output += f'{link}\n'
    print(link)

# Append the missing links to the output
for link in missing_links:
    output += f'{link}\n'
    print(link)

# Save output to a text file
outputPath = "UniqueRepositoriesOutput/uniqueRepositories.txt"
f = open(outputPath, "w")
f.write(output)
f.close()
print(f"output the repositories to: {os.path.abspath(outputPath)}")