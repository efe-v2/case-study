Insider - Case Study - Emir Faruk ERMAN

Welcome to this case study repository. I hope you enjoy it while reading both this project and the notebook 🚀

Before starting you can access to the notebook via this link https://www.kaggle.com/code/emirfarukerman/recommendation-system-final or the .ipynb file in the root of this project.

Note !! : Please check the above kaggle link for the latest version !!

## Background

My name is Emir, and I currently work as an AI & Backend engineer. Let me tell you a bit about my ML background. I graduated from Inza & Google Machine Learning Bootcamp which is a 6 month education where we learn most of the basics from neural network to reinforcement learning from Andrew Ng and Inzva Tutors, and subsequently prepared for the TensorFlow Certification of Google. After earning the certification I become a Tensorflow Developer.

I continued my journey with the Inzva Applied AI #7 program, where I learned about MLOps and deep dive to hot topic of NLP, CNN, machine learning papers.

After that, I participated in Inzva AI Projects #8, where my team and I implemented Microsoft's "Machine Unlearning in LLMs" paper from scratch, earning 3rd place. Here in the link I explain the implementation of the code and how we achieve unlearning. 
(https://www.youtube.com/watch?v=ehJauGBto8A&t=2s&ab_channel=inzvateam).

Now I am tutor of both Inzva Deep Learning study group and Applied AI 🚀

Currently, I am preparing for the AWS Machine Learning Specialty Certification to deepen my expertise in MLOps, ML development, and data processing. To put my learning into practice, I have integrated AWS technologies into this project.

So far, I have completed data engineering, exploratory data analysis, modeling, ML implementation, and MLOps parts of the [AWS Machine Learning Course](https://www.udemy.com/course/aws-machine-learning/?couponCode=LETSLEARNNOWPP). I am excited to use this knowledge to solve real time problems and make impactful contributions.


Let's Get Started 🚀 : 


The main goal of this project is to create a recommendation engine for an e-commerce website. This repository showcases a comprehensive approach to building a machine learning model that personalizes product recommendations based on user interactions.

In this project, I:

I used pre-collected data to analyze user interactions from hundreds of different e-commerce websites.

To create a recomendation system, LightFM library used to build a collaborative filtering model that can generate personalized product recommendations.

For frontend or related service to be able to get the recommendations FastAPI based application developed through a RESTful API.

Data is everything, to handle real-time user interactions an architecture designed which send user interaction data to AWS SQS, process it using AWS Lambda, and store it in S3 for further analysis and model retraining.

A CI/CD pipeline implemented to ensure code quality and functionality through automated tests and continuous integration.


The Progress:

✅ Recommendation Model Created

✅ Interaction Endopint Completed

   ✅ AWS SQS Connection (FIFO)

   ✅ AWS Lambda Connection

   ✅ AWS S3 Connection To Store File Structured Interactions
   
✅ Recommendation Endpoint Completed
   
   ✅ AWS S3 Connection For Model Files

✅ Manuel Model Updating Endpoint Completed
   
✅ Dockerization Completed

✅ Pytest implementation Completed

🔲 Kubernetes Files

🔲 Github Workflow  
   
   🔲 Github Pytest When PR to Main Workflow 
   (There is a current problem with the envirement value of repository secrets, will be fixed if any time left)

   🔲 Github Docker Deployement When Merge to Main Workflow 

🔲 Autometed Model Creation & Deployement Workflow

🔲 AWS EC2 For Deploying Model And Server

❌ AWS Kinesis For Real Time (No Free Tier)

❌ AWS Batch Process For Real Time (No Free Tier)


Getting Started: 

- Clone the repository:

git clone https://github.com/efe-v2/case-study.git
cd case-study

- Add .env file provided in the mail to the rrot of this project

- Build and run the Docker container:

docker-compose up app

Note : If you are a Mac ARM based user and want to run python test, I created docker-compose for test to run without any problem

Run the Docker Test container:

docker-compose up test

- Environment Variables::

Make sure to set the following environment variables:

- AWS_REGION
- AWS_ACCESS_KEY_ID
- AWS_SECRET_ACCESS_KEY
- SQS_QUEUE_URL

You can add these to your environment or define them in your .env file.

Once the application is running, you can access the Swager API documentation at http://localhost:5000/docs and the Redoc documentation at http://localhost:5000/redoc


## Next Steps and Gratitude

I've truly enjoyed working on this project and sharing the journey with you.

I'm eager to dive deeper into this field, experiment with advanced methods, and explore new techniques to enhance recommendation systems. There’s always more to learn and discover, and I am excited about the potential improvements and innovations ahead.

Thank you for taking the time to read through this project! Your feedback and suggestions are greatly appreciated and always welcome. 🚀