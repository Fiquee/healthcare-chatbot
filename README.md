# Healthcare Review Management Chatbot

WID3002 Natural Language Processing Group Assignment

In this assignment, we are required to build an NLP application in order to help in healthcare domain.

### Overview

- We decided to build a chatbot that will act as a platform for the end user to give feedback about the healthcare they received.
- The platform then includes an admin view for the healthcare personnel to easily identify how the patients feel based on the sentiment of their reviews and in what areas they can improve based on text classification.
- The chatbot then includes two NLP models:
  1. **Sentiment Analysis Model** to predict sentiment polarity of the reviews.
  2. **Multi-class Text Classification Model** to predict the probable categories of the reviews (a single review can be related to multiple classes).
- The classes we chose for the model to classify are:
  - Appointment
  - Facilities
  - Staff
  - Treatment
- Although a rough prototype, the resulting model showed promise and evaluation metrics in the form of precision and recall values were used to determine the best threshold at the time.

### **Dataset**

- The dataset was collected by scraping selected hospital/clinic reviews from Google Maps reviews.
- They were then manually annotated by the team members in order to form a labeled dataset for the classes and sentiment for each review.

### Model Used

- A pre-trained model by Spacy was used and further tuned with our custom dataset.

### Running the Application

1. Run the command `pip install -r requirements.txt` to install the required modules.
2. Download the application configuration files (private to the team members)
3. Place the `.env` file and the service account file in the `app` folder.
4. Run the following sequence of commands to start the app:
   ```
   cd app
   streamlit run app.py
   ```

### Application Preview

**Chatbot View**

<img src="screenshots/1_chatbot.jfif">

**Positive Review Example**

<img src="screenshots/2_sample_positive.jfif">

**Negative Review Example**

<img src="screenshots/3_sample_negative.jfif">

**Dashboard View**

<img src="screenshots/4_dashboard_1.jfif">
<img src="screenshots/5_dashboard_2.jfif">
