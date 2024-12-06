import os
import google.generativeai as genai

# Configure API Key
def configure_api():
    genai.configure(api_key="AIzaSyBvkA_FEfkJLAf2_L7nR4ogOfixLOI7vqI")  # Replace with your actual API key

# Analyze sentiment using Gemini API with fine-tuned prompt
def analyze_sentiment_with_gemini(response_text):
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        prompt = (
            f"Analyze the sentiment of the following text: '{response_text}'\n"
            f"Provide a detailed analysis of sentiment (e.g., highly positive, positive, neutral, slightly negative, highly negative) "
            f"and a numerical score from 1 to 100. Higher scores indicate positive sentiment. Output in this format:\n"
            f"Sentiment: [description]\nScore: [1-100]"
        )
        analysis = model.generate_content(prompt)
        # Extract score and sentiment from the output
        sentiment = analysis.text.split("Sentiment:")[1].split("\n")[0].strip()
        score = int(analysis.text.split("Score:")[1].strip())
        return sentiment, score
    except Exception as e:
        raise Exception(f"Error analyzing sentiment: {str(e)}")

# Perform sentiment analysis and generate only overall sentiment summary
def perform_sentiment_analysis(input_file_path, output_file_path):
    try:
        # Read responses from input file
        with open(input_file_path, 'r') as file:
            lines = file.readlines()

        total_score = 0
        count = 0
        detailed_results = []

        for line in lines:
            if "-" in line:
                question, response = map(str.strip, line.split("-", 1))
                sentiment_description, score = analyze_sentiment_with_gemini(response)
                total_score += score
                count += 1
                detailed_results.append(f"{question} - Sentiment: {sentiment_description}, Score: {score}")

        # Calculate overall sentiment score
        average_score = total_score / count if count > 0 else 50  # Default neutral score
        overall_sentiment_summary = generate_overall_summary(average_score)

        # Write the detailed results and summary to the output file
        os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
        with open(output_file_path, 'w') as output_file:
            output_file.write("Detailed Sentiment Analysis:\n")
            output_file.write("\n".join(detailed_results))
            output_file.write("\n\nOverall Sentiment Summary:\n")
            output_file.write(overall_sentiment_summary)

    except Exception as e:
        raise Exception(f"Error performing sentiment analysis: {str(e)}")

# Generate overall sentiment summary
def generate_overall_summary(average_score):
    if average_score >= 85:
        overall_sentiment = "Highly Positive"
        description = (
            "The overall responses reflect a highly positive sentiment, indicating great optimism and satisfaction. "
            "Keep up the excellent work and maintain this emotional outlook."
        )
    elif average_score >= 65:
        overall_sentiment = "Positive"
        description = (
            "The overall responses suggest a generally positive sentiment. "
            "Some areas could improve, but the outlook is overall optimistic."
        )
    elif average_score >= 45:
        overall_sentiment = "Neutral"
        description = (
            "The overall responses reflect a balanced sentiment with room for improvement. "
            "Consider focusing on areas that could enhance positivity."
        )
    elif average_score >= 25:
        overall_sentiment = "Negative"
        description = (
            "The overall responses convey a predominantly negative sentiment, indicating dissatisfaction or challenges. "
            "Address the key areas of concern to improve emotional well-being and outlook."
        )
    else:
        overall_sentiment = "Highly Negative"
        description = (
            "The overall responses show a highly negative sentiment, signaling significant dissatisfaction or challenges. "
            "Immediate attention is needed to address key areas of concern."
        )

    return f"Overall Sentiment: {overall_sentiment}\n" \
           f"Score: {int(average_score)} / 100\n" \
           f"{description}\n"

# Main function
def main():
    input_file = "ml_model/input/input.txt"  # Input file with responses
    output_file = "ml_model/output/result.txt"  # Output file for results

    # Configure the API and perform analysis
    configure_api()
    perform_sentiment_analysis(input_file, output_file)

if __name__ == "__main__":
    main()
