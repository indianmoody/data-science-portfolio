## Predicting Which Blogs are Going to Receive Most Number of Comments

This project is about predicing blogs that are going to receive most number of comments in next 24 hours. The blogs are at most 72 hours old from the time predictions are to be made. The detailed description and aim of data is available at [data source](http://archive.ics.uci.edu/ml/datasets/BlogFeedback)


### Scoring:
*Top 10* - After the predictions are made for number of comments to be received by blogs, the blogs are sorted by predicted
comment values. The predicted top 10 blogs are then compared with actual top 10 blogs (according to number of comments 
received). The score is then number of matches between these two. So, if 6 out of predicted top 10 blogs are also among actual 
top 10 blogs, the score is 6/10 i.e. 0.6 .
*Top 20* - Same as Top 10 but for top 20 blogs.
*Top 50* - Same as Top 10 but for top 50 blogs.

### Files
* *blog_analysis_quick.ipynb*: Quick analysis for data distribution, corellation and scope of answers from given data.
* *most_commented_blogs.ipynb*: Model selection for top 10, 20 and 50 blogs with most comments.

### Data Source
[BlogFeedBack Dataset UCI](http://archive.ics.uci.edu/ml/datasets/BlogFeedback)
