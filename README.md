# DS-assignment_Implementing-a-load-balancer

# Performance Evaluation and Observations

## Task Description
A-1: Launch 10,000 async requests on N = 3 server containers and report the request count handled by each server instance in a bar chart.

![Screenshot 1](https://res.cloudinary.com/dwh98o938/image/upload/v1714337744/Screenshot_2024-04-28_at_10.58.28_PM_cklsvo.png)



![Screenshot 2](https://res.cloudinary.com/dwh98o938/image/upload/v1714337745/Screenshot_2024-04-28_at_10.58.44_PM_s3vvko.png)

## Performance Evaluation

### Response Time
With 10,000 requests spread across 3 server instances, the average response time was approximately 12.07 milliseconds per request (120.66 seconds / 10,000 requests). This time includes network latency, server processing time, and response transmission back to the client.

### Concurrency and Scaling
The use of multiple server instances likely helped distribute the load and handle a higher number of concurrent requests more efficiently. This approach can enhance system scalability and responsiveness.

![Screenshot 3](https://res.cloudinary.com/dwh98o938/image/upload/v1714337745/Screenshot_2024-04-28_at_11.14.31_PM_gc5foa.png)
