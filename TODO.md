1. After you click process, you shouldn't be able to click it again / calls to process shouldn't happen. 
2. Need to properly parse the DateField values for the extraction job.
3. Processing should happen on the backend only; the /process endpoint should redirect you to the same page, but show that the job is processing.