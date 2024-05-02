# DS-assignment_Implementing-a-load-balancer

## Performance Evaluation and Observations

### Task Description (A-1):
Launch 10,000 async requests on N = 3 server containers and report the request count handled by each server instance in a bar chart.

![Screenshot 1](https://res.cloudinary.com/dwh98o938/image/upload/v1714337744/Screenshot_2024-04-28_at_10.58.28_PM_cklsvo.png)



![Screenshot 2](https://res.cloudinary.com/dwh98o938/image/upload/v1714337745/Screenshot_2024-04-28_at_10.58.44_PM_s3vvko.png)

### Performance Evaluation

#### Response Time
With 10,000 requests spread across 3 server instances, the average response time was approximately 12.07 milliseconds per request (120.66 seconds / 10,000 requests). This time includes network latency, server processing time, and response transmission back to the client.

#### Concurrency and Scaling
The use of multiple server instances likely helped distribute the load and handle a higher number of concurrent requests more efficiently. This approach can enhance system scalability and responsiveness.

![Screenshot 3](https://res.cloudinary.com/dwh98o938/image/upload/v1714337745/Screenshot_2024-04-28_at_11.14.31_PM_gc5foa.png)



### Task Description (A-2:)
Increment N from 2 to 6 and launch 10,000 requests on each such increment. Report the average load of the servers at each run in a line chart.

![Screenshot 4](https://res.cloudinary.com/dwh98o938/image/upload/v1714337745/Screenshot_2024-04-28_at_11.36.50_PM_z7nwpj.png)



![Screenshot 5](https://res.cloudinary.com/dwh98o938/image/upload/v1714337746/Screenshot_2024-04-28_at_11.23.56_PM_a69krh.png)

### Calculating Average Load

###$ Total Time and Response Time per Request
- For N = 2: Total time taken (T_2) = 131.91 seconds
- For N = 6: Total time taken (T_6) = 220.96 seconds
- Number of requests (R) = 10,000

#### Average Response Time per Request (RT)
- For N = 2: RT_2 = T_2 / R = 131.91 / 10000 = 0.013191 seconds/request
- For N = 6: RT_6 = T_6 / R = 220.96 / 10000 = 0.022096 seconds/request

### Interpretation and Discussion

#### Average Load Analysis
- RT_2 = 0.013191 seconds/request (N = 2)
- RT_6 = 0.022096 seconds/request (N = 6)

#### Scalability Implications
- **Increase in Response Time:** The average response time per request (RT) increases significantly when N is scaled up from 2 to 6.

#### Effect on Load Balancing
- With N = 2, the load balancer achieves a lower average response time per request, indicating efficient load distribution across fewer server containers.
- However, with N = 6, the average response time per request increases, suggesting potential challenges in maintaining performance and load balance across a larger number of server containers.
  
![Screenshot 6](https://res.cloudinary.com/dwh98o938/image/upload/v1714337746/Screenshot_2024-04-28_at_11.36.27_PM_fmtuhz.png)



### Task Description (A-4)/(A-1):
Launch 10,000 async requests on N = 3 server containers and report the request count handled by each server instance in a bar chart.

![Screenshot 7](https://res.cloudinary.com/dwh98o938/image/upload/v1714338774/Screenshot_2024-04-29_at_12.12.16_AM_q5wiba.png)



![Screenshot 8](https://res.cloudinary.com/dwh98o938/image/upload/v1714337745/Screenshot_2024-04-28_at_10.58.44_PM_s3vvko.png)

### Performance Evaluation

#### Average Response Time:
Calculate the average response time per request (RT) based on the reported total time taken (T) and number of requests (R):
Average Response Time (RT): RT = T / R
For example, with T = 214.74 seconds and R = 10,000 requests:
RT = 214.74 seconds / 10,000 requests = 0.021474 seconds/request (or 21.47 milliseconds/request)

#### Scalability and Concurrency:
Assess the impact of using multiple server instances (N = 3) on system scalability and responsiveness:

#### Concurrency and Scaling:
Evaluate how the use of multiple server instances distributes the load and enhances the system's ability to handle concurrent requests efficiently.
Consider the benefits of increased scalability and responsiveness achieved through load distribution among server instances.

![Screenshot 9](https://res.cloudinary.com/dwh98o938/image/upload/v1714338774/Screenshot_2024-04-29_at_12.09.26_AM_tbmzlz.png)


### Task Description (A-4)/(A-2:)
Increment N from 2 to 6 and launch 10,000 requests on each such increment. Report the average load of the servers at each run in a line chart.

![Screenshot 10](https://res.cloudinary.com/dwh98o938/image/upload/v1714340292/Screenshot_2024-04-29_at_12.11.44_AM_jnyhfu.png)



![Screenshot 11](https://res.cloudinary.com/dwh98o938/image/upload/v1714337746/Screenshot_2024-04-28_at_11.23.56_PM_a69krh.png)

####Calculating Average Load:
Total Time and Response Time per Request:
For N = 2: Total time taken (T_2) = 113.73 seconds
For N = 6: Total time taken (T_6) = 210.81 seconds
Number of requests (R) = 10,000

####Average Response Time per Request (RT):
Calculate the average response time per request for each scenario:
For N = 2: RT_2 = T_2 / R = 113.73 / 10000 = 0.011373 seconds/request
For N = 6: RT_6 = T_6 / R = 210.81 / 10000 = 0.021081 seconds/request
  
![Screenshot 12](https://res.cloudinary.com/dwh98o938/image/upload/v1714340293/Screenshot_2024-04-29_at_12.17.26_AM_wqraah.png)

Observations and Scalability Analysis:
Graph Interpretation:
The line chart displays the average response time per request (RT) as the number of server containers (N) increases from 2 to 6.
Evaluate the trend in average response times across different values of N to assess scalability.
Scalability Assessment:
Based on the graph and calculated average response times:
Increasing Load: As N increases, the average response time per request (RT) tends to increase.
Performance Impact: The observed increase in response time with higher N values suggests potential scalability limitations or inefficiencies in load distribution.
