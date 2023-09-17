import vertexai
from vertexai.language_models import TextGenerationModel
import time
import os
import csv



def get_model_prediction(description):
  vertexai.init(project="portfolio-296415", location="us-central1")
  parameters = {
      "max_output_tokens": 1024,
      "temperature": 0.2,
      "top_p": 0.8,
      "top_k": 40
  }
  model = TextGenerationModel.from_pretrained("text-bison@001")
  response = model.predict(
      f"""Read this transaction description and categorize it into one of these categories. Use the name of the category as your response.
   Auto Fees
   Auto Fuel
   Auto Parking
   Auto Repair/maintenance
   Bank service charge
   Target
   Charity
   Dining
   Beverages
   Entertainment
   Groceries
   Hobbies
   Insurance
   Bucees
   Beauty
   Medical
   Miscellaneous
   GCP bills
   Services
   Internet
   Phone
   Rent
   Subscriptions
   Taxes
   Electricity
   Water
   Salary
   Credit card payment
   Amazon
   Transfer
   Investment
   Pet Care

  Transaction Description: TX STATE PKS ADV RES 512-389-8900 TX
  Category Prediction: Entertainment

  Transaction Description: FIVE GUYS 4026 ECOMM PFLUGERVILLE TX
  Category Prediction: Dining

  Transaction Description: TST* WEST PECAN COFFEE A PFLUGERVILLE TX
  Category Prediction: Beverages
  
  Transaction Description:Oakville OBSIDIAN.MD              OAKVILLE     ON
  Category Description: Subscriptions

  Transaction Description:PAYPAL *STEAM GAMES 402-935-7733 WAUSA
  Category Description: Hobbies

  Transaction Description: {description}
  Category Prediction:
  """,
      **parameters
  )
  print(f"Description:{description}\nResponse from Model: {response.text}\n----=========----\n")
  # quota is 60 requests per minute
  time.sleep(2)
  return response.text


def process_csv_file(file_path):
    output_rows = []
    
    with open(file_path, 'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        header = reader.fieldnames
        
        if 'LLM description' in header:
            print(f"File {file_path} already has an 'LLM description' column.")
        else:
          header.append('LLM description')  # Add the new column

        output_rows.append(header)
        
        for row in reader:
            description = row['Description']
            if "Original Description" in row:
                description += " " + row["Original Description"]
            llm_description = row.get('LLM description', None)  # Check if LLM description exists
            
            if llm_description is None or llm_description == "None":
                try:
                    llm_description = get_model_prediction(description)
                except Exception as e:
                    llm_description = "None"
                
                row['LLM description'] = llm_description
                output_rows.append([row[field] for field in header])
                
    # Write intermediate results to the file
    with open(file_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(output_rows)
    
    print(f"Processed {file_path} and updated 'LLM description' column.")

def main():
  csv_files = [file for file in os.listdir('.') if file.endswith('.csv')]
  csv_files.sort(key=lambda x: os.path.getmtime(x), reverse=True)
  
  print("Select a CSV file to process:")
  for idx, file in enumerate(csv_files, start=1):
      print(f"{idx}. {file}")
  
  choice = None
  while choice is None:
      try:
          choice = int(input("Enter the number of the file to process: "))
          if not 1 <= choice <= len(csv_files):
              raise ValueError
      except ValueError:
          print("Invalid choice. Please enter a valid number.")
          choice = None
  
  selected_file = csv_files[choice - 1]
  
  process_csv_file(selected_file)
  print(f"Processed {selected_file} and updated descriptions.")
  
if __name__ == "__main__":
    main()
