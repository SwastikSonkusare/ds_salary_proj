from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from selenium import webdriver
import time
import pandas as pd
import numpy as np
from selenium.webdriver.common.by import By


def get_jobs(num_jobs, verbose):
    '''Gathers jobs as a dataframe, scraped from Glassdoor'''

    # Initializing the webdriver
    options = webdriver.ChromeOptions()

    # Uncomment the line below if you'd like to scrape without a new Chrome window every time.
    # options.add_argument('headless')

    # Change the path to where chromedriver is in your home folder.
    driver = webdriver.Chrome(
        executable_path="C:/Program Files/Chrome driver/chromedriver.exe", options=options)
    driver.set_window_size(1120, 1000)
    
    url = 'https://www.glassdoor.co.in/Job/india-data-scientists-jobs-SRCH_IL.0,5_IN115_KO6,21.htm?suggestCount=0&suggestChosen=false&clickSource=searchBtn&typedKeyword=&typedLocation=India&context=Jobs&dropdown=0'


#     url = 'https://www.glassdoor.co.in/Job/mumbai-data-scientist-jobs-SRCH_IL.0,6_IC2851180_KO7,21.htm?suggestCount=0&suggestChosen=false&clickSource=searchBtn&typedKeyword=data%2520scientist&typedLocation=Mumbai&context=Jobs&dropdown=0'
    driver.get(url)
    jobs = []

    # If true, should be still looking for new jobs.
    while len(jobs) < num_jobs:

        # Let the page load. Change this number based on your internet speed.
        # Or, wait until the webpage is loaded, instead of hardcoding it.
        time.sleep(4)

        # Test for the "Sign Up" prompt and get rid of it.

        try:
            driver.find_element(
                by=By.XPATH, value="//*[@id='MainCol']/div[1]/ul/li[1]").click()
        except ElementClickInterceptedException:
            pass

        time.sleep(3)

        try:
            # clicking to the X.
            driver.find_element(
                By.CSS_SELECTOR, 'span.modal_closeIcon').click()
        except NoSuchElementException:
            pass

        # Going through each job in this page
        # jl for Job Listing. These are the buttons we're going to click.
        job_buttons = driver.find_elements(By.CLASS_NAME, "react-job-listing")
        for job_button in job_buttons:

            print("Progress: {}".format(
                "" + str(len(jobs)) + "/" + str(num_jobs)))
            if len(jobs) >= num_jobs:
                break

            job_button.click()  # You might
            time.sleep(1)
            collected_successfully = False

            while not collected_successfully:
                try:
                    try:
                        company_name = driver.find_element(
                            By.XPATH, value='//*[@id="JDCol"]/div/article/div/div[1]/div/div/div[1]/div[3]/div[1]/div[1]').text
                        # print(f'Company name is {company_name}')
                    except NoSuchElementException:
                        print("Company name not found")

                    try:
                        location = driver.find_element(
                            By.XPATH, value='//*[@id="JDCol"]/div/article/div/div[1]/div/div/div[1]/div[3]/div[1]/div[1]/following-sibling::div[2]').text
                        # print(f'Location is {location}')
                    except NoSuchElementException:
                        print("Location not found")

#                     job_title = driver.find_ele(by=By., value='.//div[contains(@class, "title")]').text

                    try:
                        job_title = driver.find_element(
                            by=By.CLASS_NAME, value='css-1vg6q84').text
                        # print(f'Job title  is {job_title}')
                    except:
                        print("Job title not found")

                    try:
                        job_description = driver.find_element(
                            by=By.XPATH, value='.//div[@class="jobDescriptionContent desc"]').text
                        # print(f'Job desc is {job_description}')
                    except NoSuchElementException:
                        print("Description not found")
                    collected_successfully = True
                except:
                    time.sleep(5)

            try:
                salary_estimate = driver.find_element(
                    By.XPATH, value='//*[@id="JDCol"]/div/article/div/div[1]/div/div/div[1]/div[3]/div[1]/div[1]/following-sibling::div[3]/span[1]').text
                # print(f'Salary is {salary_estimate}')
            except NoSuchElementException:
                salary_estimate = np.NaN  # You need to set a "not found value. It's important."
                print("Salary not found")

            try:
                rating = driver.find_element(
                    By.XPATH, '//*[@id="employerStats"]/div[1]/div[1]').text
                # print(f'Rating is {rating}')
            except NoSuchElementException:
                rating =  np.NaN  # You need to set a "not found value. It's important."
                print("Rating not found")

            # Printing for debugging
            if verbose:
                print("Job Title: {}".format(job_title))
                print("Salary Estimate: {}".format(salary_estimate))
                print("Job Description: {}".format(job_description[:500]))
                print("Rating: {}".format(rating))
                print("Company Name: {}".format(company_name))
                print("Location: {}".format(location))

            # Going to the Company tab...
            # clicking on this:
            #
# Company

            try:
                try:
                    # size = driver.find_element(by=By.XPATH, value='.//div[@class="infoEntity"]//label[text()="Size"]//following-sibling::*').text
                    size = driver.find_element(
                        by=By.XPATH, value='//*[@id="EmpBasicInfo"]/div[1]/div[1]/div[1]/span[2]').text
                except NoSuchElementException:
                    print("size not found")
                    size = np.NaN
                try:
                    # founded = driver.find_element(
                    #     by=By.XPATH, value='.//div[@class="infoEntity"]//label[text()="Founded"]//following-sibling::*').text
                    founded = driver.find_element(
                        by=By.XPATH, value='//*[@id="EmpBasicInfo"]/div[1]/div[1]/div[2]/span[2]').text
                except NoSuchElementException:
                    print("founded not found")
                    founded = np.NaN

                try:
                    # type_of_ownership = driver.find_element(
                    #     by=By.XPATH, value='.//div[@class="infoEntity"]//label[text()="Type"]//following-sibling::*').text
                    type_of_ownership = driver.find_element(
                        by=By.XPATH, value='//*[@id="EmpBasicInfo"]/div[1]/div[1]/div[3]/span[2]').text
                except NoSuchElementException:
                    print("ownership not found")
                    type_of_ownership = np.NaN

                try:
                    # industry = driver.find_element(
                    #     by=By.XPATH, value='.//div[@class="infoEntity"]//label[text()="Industry"]//following-sibling::*').text
                    industry = driver.find_element(
                        by=By.XPATH, value='//*[@id="EmpBasicInfo"]/div[1]/div[1]/div[4]/span[2]').text
                except NoSuchElementException:
                    print("industry not found")
                    industry =  np.NaN

                try:
                    # sector = driver.find_element(
                    #     by=By.XPATH, value='.//div[@class="infoEntity"]//label[text()="Sector"]//following-sibling::*').text
                    sector = driver.find_element(
                        by=By.XPATH, value='//*[@id="EmpBasicInfo"]/div[1]/div[1]/div[5]/span[2]').text
                except NoSuchElementException:
                    print("sector not found")
                    sector =  np.NaN

                try:
                    # revenue = driver.find_element(
                    #     by=By.XPATH, value='.//div[@class="infoEntity"]//label[text()="Revenue"]//following-sibling::*').text
                    revenue = driver.find_element(
                        by=By.XPATH, value='//*[@id="EmpBasicInfo"]/div[1]/div[1]/div[6]/span[2]').text
                except NoSuchElementException:
                    revenue =  np.NaN

            # Rarely, some job postings do not have the "Company" tab.
            except NoSuchElementException:
                size =  np.NaN
                founded =  np.NaN
                type_of_ownership =  np.NaN
                industry =  np.NaN
                sector =  np.NaN
                revenue =  np.NaN

            if verbose:
                # print("Headquarters: {}".format(headquarters))
                print("Size: {}".format(size))
                print("Founded: {}".format(founded))
                print("Type of Ownership: {}".format(type_of_ownership))
                print("Industry: {}".format(industry))
                print("Sector: {}".format(sector))
                print("Revenue: {}".format(revenue))
                # print("Competitors: {}".format(competitors))
                print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")

            jobs.append({"Job Title": job_title,
                         "Salary Estimate": salary_estimate,
                         "Job Description": job_description,
                         "Rating": rating,
                         "Company Name": company_name,
                         "Location": location,
                        #  "Headquarters": headquarters,
                         "Size": size,
                         "Founded": founded,
                         "Type of ownership": type_of_ownership,
                         "Industry": industry,
                         "Sector": sector,
                         "Revenue": revenue,
                         #  "Competitors": competitors
                         })
            # add job to jobs

        # Clicking on the "next page" button
        try:
            driver.find_element(By.CLASS_NAME, 'nextButton').click()
        except NoSuchElementException:
            print("Scraping terminated before reaching target number of jobs. Needed {}, got {}.".format(
                num_jobs, len(jobs)))
            break

    # This line converts the dictionary object into a pandas DataFrame.
    return pd.DataFrame(jobs)


df = get_jobs(1200, False)
df.to_csv('./glassdoor_jobs_3.csv')
