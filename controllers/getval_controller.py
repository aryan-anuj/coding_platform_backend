import requests
from flask import jsonify
from utils.data_cleaning import clean_data2
from config import read_api

def get_feild_data(channel_id, fields):
    try:
        nodejs_response = requests.get(read_api.format(channel_id=channel_id))
        nodejs_data = nodejs_response.json()

        if 'entries' not in nodejs_data:
            return jsonify({"error": "No entries found for the given channel ID"}), 404

        result_data = {}
        missing_fields = []

        for field in fields:
            data = clean_data2(nodejs_data['entries'], field)
            if data is None or data.empty:
                missing_fields.append(field)
            else:
                # Get the last entry for the field
                last_entry = data.tail(1).to_dict(orient='records')[0]
                result_data[field] = last_entry

        response = {"data": result_data}

        if missing_fields:
            response["message"] = {"no_data": f"No data found for these fields: {', '.join(missing_fields)}"}

        return jsonify(response)

    except Exception as e:
        return jsonify({"error": str(e)}), 500
