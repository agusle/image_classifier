                                                                                                    Agustín Leperini
                                                                                                    06.06.22
---
# ML API - Stress Test Report
## Introduction 

In this stress test I'm simulating the use of the app following endpoints:
- /index
- /predict

By using the tool [Locust](https://locust.io/) we managed to create different scenarios of users traffic. I used different scales for each endpoint, increasing *"/predict"* three times than *"/index"* because of the intended use.

## Hardware specifications of localhost:
#### CPU:
Processor AMD Ryzen 5 2500U with Radeon Vega Mobile Gfx, 2000 Mhz, 4 Core(s), 8 Logical Processor(s).  
*Without running any test the percentage of cpu used was around 57%.*

#### Memory:  
Installed physical memory (RAM): 12.0 GB  
Local Disk (Solid state disk - SSD) free space: 37.9 GB  
*Without running any test the percentage of cpu used was around 78%.*

## Test 1
#### 4 rounds tested with only one ML_service deployed:

1. Round 1: 3 users - 1 spawn/sec (CPU 60% and Memory 80%)_[*more details*](https://htmlpreview.github.io/?https://github.com/anyoneai/sprint-4-project/blob/AgustinLeperini_assignment/stress_test/Locust_html/report_AgusLep_locust_3-1_scale1.html)
2. Round 2: 10 users - 1 spawn/sec (CPU 62% and Memory 81%)_[*more details*](https://htmlpreview.github.io/?https://github.com/anyoneai/sprint-4-project/blob/AgustinLeperini_assignment/stress_test/Locust_html/report_AgusLep_locust_10-1_scale1.html)
3. Round 3: 100 users - 1 spawn/sec (CPU 62% and Memory 82%)_[*more details*](https://htmlpreview.github.io/?https://github.com/anyoneai/sprint-4-project/blob/AgustinLeperini_assignment/stress_test/Locust_html/report_AgusLep_locust_100-1_scale1.html)
4. Round 4: 600 users - 1 spawn/sec (CPU 66% and Memory 86%)_[*more details*](https://htmlpreview.github.io/?https://github.com/anyoneai/sprint-4-project/blob/AgustinLeperini_assignment/stress_test/Locust_html/report_AgusLep_locust_600-1_scale1.html)

- Ping and first failures: __from 46 users at about 4 rps.__  
- */predict* endpoint breakdown: __from 550 users at about 5 rps.__  

![scale1](/stress_test/locust_report_scale1.PNG)

## Test 2
#### 3 rounds tested with three ML_service deployed:

1. Round 1: 10 users - 1 spawn/sec (CPU 62% and Memory 81%)_[*more details*](https://htmlpreview.github.io/?https://github.com/anyoneai/sprint-4-project/blob/AgustinLeperini_assignment/stress_test/Locust_html/report_AgusLep_locust_10-1_scale3.html)
2. Round 2: 100 users - 1 spawn/sec (CPU 64% and Memory 83%)_[*more details*](https://htmlpreview.github.io/?https://github.com/anyoneai/sprint-4-project/blob/AgustinLeperini_assignment/stress_test/Locust_html/report_AgusLep_locust_100-1_scale3.html)
3. Round 3: 1000 users - 2 spawn/sec (CPU 71% and Memory 89%)_[*more details*](https://htmlpreview.github.io/?https://github.com/anyoneai/sprint-4-project/blob/AgustinLeperini_assignment/stress_test/Locust_html/report_AgusLep_locust_1000-2_scale3.html)

- Ping and first failures: __from 77 users at about 5.3 rps.__  
- */predict* endpoint breakdown: __from 615 users at about 6.2 rps.__

![scale3](/stress_test/locust_report_scale3.PNG)