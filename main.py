from ai.embeddings_to_recommendation_json import extract_recommendation_from_file
from web.json_data_to_html import html_to_file
from fetch.target_date import QueryDate
from common.logger import Logger
from web.fetch.main import setup
from common.paths import remove_dir
from common.paths import Paths

if __name__ == "__main__":
    query_date = QueryDate.Today

    remove_dir(Paths.DATA_DIR)
    setup(query_date)

    recommendation_count = extract_recommendation_from_file(threshold=.85)
    Logger.log(f"found: {recommendation_count} recommendation(s)")

    output_html_location = html_to_file()
    Logger.log(f"see results at: {output_html_location}")

