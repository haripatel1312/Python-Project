from bs4 import BeautifulSoup
import requests
import random
import openpyxl

def get_user_input():
    # Use of While
    while True:
        a = input("Enter a year (between 1900 and 2023): ")
        year = int(a)

        # Validate the User Input
        if 1900 <= year <= 2100:
            return a
        else:
            print("Invalid input. Please enter a valid year (between 1900 and 2023).")

def scrape_movies_by_year(year):
    # Define a list of User Agents for different browsers
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:53.0) Gecko/20100101 Firefox/53.0',
        'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0; Trident/5.0)',
        'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0; MDDCJS)',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393',
        'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1)'
    ]

    # Get the data from the Wikipedia page and store it in the source variable
    source = requests.get('https://en.wikipedia.org/wiki/List_of_highest-grossing_films', headers={'User-Agent': random.choice(user_agents)})
    source.raise_for_status()

    soup = BeautifulSoup(source.text, 'html.parser')
    tbody = soup.find('tbody')

    # Exception handling
    try:
        # List to store movies by year
        movies_by_year = []

        # Iterate through rows in the table, skipping the header row.
        for row in tbody.find_all('tr')[1:]:
            columns = row.find_all('td')

            # Get rank, peak, title, gross, and year.
            title_tag = row.find('a')
            Title = title_tag.text.strip()
            rank = columns[0].text.strip()
            peak = columns[1].text.strip()
            Gross = columns[2].text.strip()
            Year = columns[3].text.strip()

            # Check if the year matches user input
            if Year == year:
                movies_by_year.append({
                    'Rank': rank,
                    'Peak': peak,
                    'Title': Title,
                    'Gross': Gross,
                    'Year': Year
                })

        # Return the list of movies by year
        return movies_by_year  

    except requests.exceptions.RequestException as req_error:
        print(f"Request failed: {req_error}")

    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# Function to display movies to the user
def display(movies):
    print()
    print(f"Films released in {year_input}:")
    print()
    for movie in movies:
        print(f"Rank: {movie['Rank']}")
        print(f"Peak: {movie['Peak']}")
        print(f"Title: {movie['Title']}")
        print(f"Gross Revenue: {movie['Gross']}")
        print(f"Year: {movie['Year']}")
        print()

# Function to write data to Excel
def write_to_excel(movies, filename='movies_data.xlsx'):
    wb = openpyxl.Workbook()
    sheet = wb.active

    # Write header row
    header = ['Rank', 'Peak', 'Title', 'Gross Revenue', 'Year']
    sheet.append(header)

    # Write data rows
    for movie in movies:
        row_data = [movie['Rank'], movie['Peak'], movie['Title'], movie['Gross'], movie['Year']]
        sheet.append(row_data)

    wb.save(filename)
    print(f"Data written to {filename}")

# Get year of user input and scrape results for that year
year_input = get_user_input()
movies = scrape_movies_by_year(year_input)

# Check if movies are found for the specified year
if movies:
    # Display movies to the user
    display(movies)

    # Create Excel file and write data
    write_to_excel(movies, filename=f'movies_by_year_{year_input}.xlsx')

else:
    print(f"No movies found for the specified year {year_input}.")
