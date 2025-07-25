
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.metrics import accuracy_score,classification_report,confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt

# Load dataset
# Replace 'your_path_here.csv' with the correct path to your dataset
fake = pd.read_csv("your_path_here")
real = pd.read_csv("your_path_here")

# label the data
fake['label'] = 0
real['label'] = 1

# combine and shuffle the data
data=pd.concat([fake,real])
data=data.sample(frac=1).reset_index(drop=True)

# prepare the features and labels
x=data['text']
y=data['label']

# convert text to numbers
vectorizer=TfidfVectorizer(stop_words='english',max_features=5000)
x_vectorized=vectorizer.fit_transform(x)

# train/test split
x_train,x_test,y_train,y_test=train_test_split(x_vectorized, y, test_size=0.2,random_state=42)

# train svm model
model=LinearSVC()
model.fit(x_train,y_train)

# predictions
y_pred=model.predict(x_test)

# evaluation
print("Accuracy :",accuracy_score(y_pred,y_test))
print("\nClassification Report :\n",classification_report(y_pred,y_test))

cm=confusion_matrix(y_pred,y_test)
# plot using seaborn
sns.heatmap(cm,annot=True,fmt='d',cmap='Blues',
            xticklabels=['Predicted Fake','Predicted Real'],
            yticklabels=['Actual Fake','Actual Real'])
plt.title("Confusion Matrix")
plt.xlabel("Predicted Labels")
plt.ylabel("Actual")
plt.show()
plt.pause(3)
plt.close()

# predict custom input
def predict_news(text):
  text_vector=vectorizer.transform([text])
  prediction=model.predict(text_vector)[0]
  return "Real News" if prediction==1 else "Fake news"

while True:
    user_input = input("\nEnter a news article or headline (or type 'exit' to quit):\n")
    if user_input.lower() == 'exit':
        break
    print("The news is :", predict_news(user_input))
