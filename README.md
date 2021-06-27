installation 
1. create env by using command    python3 -m venv env  
2. activate env.   source env/bin/activate    
3. install requirements  pip install -r requirements.txt




parameters for the bot are in .env (environ) file. 
I wrote two bots, one is asynchronous, and another is synchronous.  First one performs script faster, but with big params in env, it brokes Django's pipeline,
the second bot is much slower, but it is stable.
