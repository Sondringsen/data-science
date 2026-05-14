## Problem Setup

We formulate the problem of running an optimal marathon as a Markov Decsion Problem (MDP). 

### State
We define the state as:
$S_t = (d_t, e_t, rd_t, re_t, r_t, c_t)$ where 
- $d_t \in \mathbb{R}$ is the distance between the current point $t$ and the next point at time $t + 1$. Since the points are very close, we use the Euclidean distance instead of Haversine formula.
- $e_t \in \mathbb{R}$ is the elevation between the current point $t$ and the next point at time $t + 1$. 
- $rd_t \in \mathbb{R}$ is the remaining distance at time $t$.
- $re_t \in \mathbb{R}$ is the remaining elevation at time $t$.
- $h_t \in \mathbb{R}$ is the heart rate at time $t$.
- $c_t \in \mathbb{R}$ is the calorie surplus at tim $t$ this variable start at some $c_0$ depending on how well we have carb loaded. Negative values mean we are in calorie deficit.
- $T_t \in \mathbb{R}$ is the total time elapsed.
- $D_t \in \mathbb{R}$ is the total distance since start.

A couple of things to notice:
- We can have forward looking state variables as we know the exact route ahead of time. 
- All of these variables fall within some range we discretized to make the problem discrete. However, for this problem we treat them as continuous on the real line.
- All indices $t$ refer to the index of time, not the actual time elapsed since start.


### Action
We define the action space as:
$ A_t = (v_t, i_t)$ 
where
- $v_t \in \{0.0, 0.2, \dots, 20.0\}$ is the velocity to maintain between the current point $t$ and the next point $t + 1$. Notice that we discretiz the action space. This is because we want to use DQN. 
- $i_t \in \{0, 1\}$ is an indicator of whether to eat at time $t$. We assume that eating gives you a fixed amount of calories (this is slighly inaccurate, see [reward section](### Reward Function) for more details on this).


### Transition Probabilies
In this setup we treat all variables as deterministic. An obvious extension is to add uncertainties to formulas to make the problem probabilistic. 
$(S_t, A_t) \to S_{t+1} = (d_{t+1}, e_{t+1}, rd_{t+1}, re_{t+1}, f_h(e_t, v_t), c_t - f_c(d_t, e_t, v_t) + 75A_t)$
Where
- $f_h$ is a function that takes in a heartrate and a velocity and outputs a new heartrate.
- $f_c$ is a cost function that takes in distance and elevation in the previous step and outputs the cost in terms of calories.
- We also assume you get $75$ calories if you decide to eat. This corresponds to about $5$ Seigmenn which weighs about $5$ grams and contain about $15$ kcal each.





[@Minetti2002] finds that the metabolic cost of walking and running depends on terrain. The cost of walking also depends on speed, while the cost of running depends . Their setup considers $10$ males at around age $30$ with mean $\text{VO}_2$-max at $68.9$. They ran polynomial regression of order 5 and found two formulas explaining the cost of walking and running with $R^2 =0.999$ in both cases. 

$$
C_w(i) = 280.5i^5 - 58.7i^4 - 76.8i^3 + 51.9i^2 + 19.6i + 2.5\\
C_r(i) = 155.4i^5 - 30.4i^4 - 43.4i^3 + 46.3i^2 + 19.5i + 3.6
$$
Where $i$ is the incline or slope.

Note: the very high level of $\text{VO}_2$-max makes them elite athletes so the formulas for cost might not apply to us, but we will use them anyway. 

Assuming walking is speed under $5$ km/h and running is speed above $5$ km/h we can now define $f_c$ as:
$$
f_c(d_t, e_t, v_t) = \chi_{\{v_t \leq 5 \text{km/h}\}} C_w(\frac{e_t}{d_t}) + \chi_{\{v_t \geq 5 \text{km/h}\}} C_r(\frac{e_t}{d_t})
$$
The unit here is $\frac{J}{kg \cdot m}$. From this we can calculate the power needed as $P = f_c(d_t, e_t, v_t)\cdot v_t$ with units $\frac{J}{s}$. Now for every watt produced you need about 

- $VO2 = P \cdot 60 \frac{\text{s}}{\text{min}}/20.9 \frac{\text{J}}{\text{ml O2}}$
- $\text{Total Caloric Burn (kcal/min)} = \frac{VO_2 \cdot M}{1000}5 = \frac{VO_2 \cdot M}{200}$. The $5$ is 1 liter of $O_2 \approx 5$ kcal.
- $HR_{\text{target}} = HR_{\text{rest}} + (\frac{HR_{\text{max}} - HR_{\text{rest}}}{VO2_{\text{max}} - VO2_{\text{rest}}})(VO2 - VO2_{\text{rest}})$ 



### Reward Function
The reward function consist of a few different components. We want the reward function to at least consider the following:
- Too high heart rate should be penalized. In a more realistic setting we would rather have that a too high heart rate over a certain time period is bad and not necesserialy bad to have it for a short time. However, this would make the state space much bigger as you would need to make previous times a part of the current state.
- Too big calorie deficit should be penalized. This should be a function that becomes increasingly worse as you deplete your glycogen stores. Indeed, [@Holloszy1996] find that even in "fight or flight" situations, individuals whose muscles are glycogen depleted are unable to either run or fight.
- Eating gives you less calories when you have higher heart rate. A formula for this was hard to find, so we will just use one that makes sense. Even with lower heart rate there are phyiscal limits to what your body can absorb [@Jeukendrup2014]. 
- Not making cutoff times should be penalized heavily. 
- Finishing faster should be rewarded.


$$
R(S_t, S_{t+1}) = \gamma_1R_c(c_t) + \gamma_2R_t(d_t) + \gamma_3R_h(h_t)
$$

Each of the terms in the formula above are explained in greater detail below. Each $\gamma_i$ is a scaling factor so we can scale each contributin term appropriately. 
The reward for calories is a simple formula that penalizes eating too much and too little. The penality is squared to penalize far from $0$ heavily as a serious calorie deficit and surplus is detrimental.
$$
R_c(S_t, A_t) = (\chi_{\{c_{t+1} \geq 200\}}c_{t+1}^2 + \chi_{\{c_{t+1} \leq 200\}}c_{t+1}^2)
$$
Where $\chi$ is the indicator function.

There are four cutoffs for the 32km distance:
- 9km within 3h
- 16km within 5h
- 24km within 7h
- 32km within 9h
$$
R_t(T_t, D_t) = - \infty (\chi_{\{T_t \geq 3\text{h}, D_t \leq 9\text{km}\}} + \chi_{\{T_t \geq 5\text{h}, D_t \leq 16\text{km}\}} + \chi_{\{T_t \geq 7\text{h}, D_t \leq 24\text{km}\}} + \chi_{\{T_t \geq 9\text{h}, D_t \leq 32\text{km}\}}) - T_t
$$
The first four terms represents cutoff and the last is a linear reward incentivizing finishing faster. The scaling $\gamma_2$ will only really affect the last term as the other terms are either $0$ or $\infty$.

For the heartrate you are penalized with a square term up to some $h_{\text{max}}$. Beyond that you are penalized infinitely to basically make this a hard constraint.
$$
R_h(h_t) = -\chi_{\{h_t \geq h_\text{max}\}} \infty - h_t^2
$$



### MDP Formulation
Our goal is to find a policy $\pi$ that maximizes the reward.

$$
\pi^* = \argmax{}
$$

Since we care about finish times and , we set the discount rate $\gamma = 1.0$. We can do this since this is a finite horizon time problem.


Before we can define the states we need to define a few variables first.

We define the following variables:
- $\text{dlat}$ is the difference in latitude between two points
- $\text{dlon}$ is the difference in longitude between two points
- $\text{dx}$ is the horizontal distance between two points. 
- $\text{dy}$ it the vertical distance between two points. 

