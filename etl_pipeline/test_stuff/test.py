import json
from datetime import datetime, timedelta

# def load_city_coordinates(filepath="etl_pipeline/city_coordinates.json"):
#     try:
#         with open(filepath, "r") as f:
#             data = json.load(f)
#             for city_info in data:
#                 yield city_info
#     except FileNotFoundError:
#         print(f"File not found: {filepath}")
#     except json.JSONDecodeError as e:
#         print(f"Failed to parse JSON: {e}")

if __name__ == "__main__":
    # for city in load_city_coordinates():
    #     print(city)

    # curr_date = datetime(2024, 1, 1)
    # print(curr_date)
    # print(curr_date+1)
    # print(type(curr_date))

    # ============================================================================

    # start_date = "2022-02-25"
    # end_date = "2022-03-01"

    # # Convert strings to date objects
    # curr_date = datetime.strptime(start_date, "%Y-%m-%d").date()
    # end_date = datetime.strptime(end_date, "%Y-%m-%d").date()

    # # Loop through each date
    # while curr_date <= end_date:
    #     print(curr_date)
    #     print(curr_date.strftime("%Y-%m-%d"))
    #     print(type(curr_date.strftime("%Y-%m-%d")))
    #     curr_date += timedelta(days=1)

    # ============================================================================
    
    from datetime import datetime, timedelta

    # Get today's date
    # today = datetime.today()

    # # Subtract one day
    # yesterday = today - timedelta(days=1)

    # # Format as YYYY-MM-DD
    # formatted_yesterday = yesterday.strftime("%Y-%m-%d")


    formatted_yesterday = (datetime.today() - timedelta(days=1)).strftime("%Y-%m-%d")
    print(formatted_yesterday)
