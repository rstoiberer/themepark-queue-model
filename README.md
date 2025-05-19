# 🎢 FastPass+ Queue Simulation  

This project models Disney’s former **FastPass+ virtual queueing system** using a priority-based M/M/1 queue. By simulating different FastPass allocation levels, the system estimates **average residence times** for FastPass holders (high priority) and regular customers (low priority) under both low and high system load conditions.

The simulator helps determine how many FastPasses can be distributed **without significantly degrading the experience** for either customer group.

## 📚 Project Context

From 1999 to 2021, Disney offered FastPasses to let visitors **skip regular queues** by arriving at pre-scheduled times. FastPass holders entered a shorter line, jumping ahead of regular customers — creating a **two-class queuing system**.

From a modeling perspective, this is a **priority queue**, where:
- **FastPass customers** are always served before regular ones
- **Regular customers** are repeatedly bypassed, increasing their wait times

The central design question:  
👉 *How many FastPasses can you issue before regular customer experience becomes unacceptable?*

## 🧪 Simulation Model

- **Queue type:** M/M/1 (single-server, exponential interarrival and service times)
- **Customer classes:** FastPass (high priority) and Regular (low priority)
- **Queue behavior:**
  - FastPass holders wait only behind other FastPass holders
  - Regular customers wait behind everyone
- **Server behavior:** First-Come-First-Served (FCFS), non-preemptive
- **Arrival rates (λ):** 0.50 (low load) and 0.95 (high load)
- **Service rate (μ):** 1.0 → average service time `s = 1 minute`

The simulation runs for 50,000 minutes (with a 5,000-minute warm-up), and computes average **residence times** (waiting + service) for each group as the **FastPass fraction `f`** varies from `0` to `0.95`.

## Sample Outuputs 

![fastpass_results](https://github.com/user-attachments/assets/0a9f92eb-e135-401d-bab9-05ec94618c02)

```
Results for λ=0.5:
Recommended FastPass fraction: 0.95
  - FastPass residence time: 1.95 minutes
  - Regular residence time: 2.84 minutes
  - Regular/FastPass time ratio: 1.46

Results for λ=0.95:
Recommended FastPass fraction: 0.65
  - FastPass residence time: 3.42 minutes
  - Regular residence time: 49.15 minutes
  - Regular/FastPass time ratio: 14.39
```

## 🎯 Goal

Find a **balanced FastPass allocation fraction `f`** that:
- Keeps FastPass wait times short (the main goal)
- Avoids punishing regular customers with extreme delays
- Adjusts appropriately for high- and low-utilization periods

## 🙏 Credits

This project was inspired by and based on starter code provided by  
**Dr. Dan S. Myers**, Rollins College for the course **Simulation & Stochastic**.

## How to Run the Simulation

### 1. Clone the Repository
```
git clone https://github.com/rstoiberer/themepark-queue-model.git
cd themepark-queue-model
```

### 2. Install Dependencies
```
pip install -r requirements.txt
```
### 3. Run simulation
```
python3 fastpass_simulator.py
```

### 4. Run visualization (if desired)
```
python3 visualization_fastpass.py
```

