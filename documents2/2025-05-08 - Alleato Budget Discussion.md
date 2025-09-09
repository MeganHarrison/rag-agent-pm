# Alleato Budget Discussion
**Meeting ID**: 01JTR1YCSRVRDRKXVXDKRQAN60
**Date**: 2025-05-08
**Duration**: 16.559999465942383 minutes
**Transcript**: [View Transcript](https://app.fireflies.ai/view/01JTR1YCSRVRDRKXVXDKRQAN60)
**Participants**: bclymer@alleatogroup.com, evan.schulte@jobplanner.com, fnjie@thinkplumb.com, jdawson@alleatogroup.com, jmendez@alleatogroup.com, mcalcetero@alleatogroup.com

## Transcript
**Bclymer**: Oh, there's Brandon.
**Evan.schulte**: Hey, Brandon.
**Fnjie**: Hey.
**Fnjie**: How are you?
**Jdawson**: Good.
**Evan.schulte**: Yourself?
**Fnjie**: Doing well.
**Fnjie**: Doing well.
**Evan.schulte**: Good.
**Bclymer**: Then it looks like Jesse accepted.
**Fnjie**: Don't worry about that.
**Bclymer**: Okay.
**Bclymer**: And Maria?
**Fnjie**: Don't worry about that.
**Fnjie**: We can go ahead and start.
**Bclymer**: Oh, okay.
**Jdawson**: Okay, cool.
**Jdawson**: Sorry, Chris.
**Jdawson**: Christian, do you mind if we can record this meeting just for review?
**Fnjie**: We're already, we're already recording it, Jose.
**Jdawson**: Okay.
**Evan.schulte**: Yeah, we can, we can share that with you.
**Evan.schulte**: Christian, can you, can you just confirm that?
**Bclymer**: Yep.
**Bclymer**: Right now.
**Evan.schulte**: All right, sounds good.
**Evan.schulte**: So, yeah, yesterday we got an email that there were some budget line items and that's what we're looking at right here that showed up on the project.
**Evan.schulte**: And I'm showing that basically it looks like what happened is there were some transactions that were associated with this task here.
**Evan.schulte**: If I just bring up, I'll bring up this one here, which is a very obvious example.
**Evan.schulte**: So you've got two air charter expenses that were logged in and they're associated with the 24115 Project Task rather than the project project task.
**Evan.schulte**: And I know we had talked about on our last call this being something that it just, you know, it can't happen because if it does get imported this way, it's going to get imported in a job planner that way we're importing it, you know, identical to what Acumatica has.
**Evan.schulte**: Now.
**Evan.schulte**: There were some previous ones that we had that had imported and were zeroed out and we basically kind of made the system ignore those.
**Evan.schulte**: But because these lines are now exceeding zero, they're not zero dollars anymore.
**Evan.schulte**: Our system can't ignore them, obviously, because it needs to have those to have an accurate bottom line.
**Evan.schulte**: So I'm hoping that one, you know, we can get these addressed and as long as we can get these expenses basically recoded to the correct project task that will automatically come into job planner.
**Evan.schulte**: We can get these budget line items removed.
**Evan.schulte**: That dollar amount is going to go to the right line item and you know, that these will just, we, we can get rid of these lines.
**Evan.schulte**: If that happens going forward though, I'm hoping, you know, we can figure out what, what's causing that to happen and is there some automated system or something, you know what.
**Evan.schulte**: And resolve that so it doesn't continue.
**Fnjie**: Yeah, so that's the thing is like, you know, trying to figure out how this works and why it's doing this.
**Evan.schulte**: So I can kind of explain, you know, and from the Acumatica side too, I can show you that.
**Evan.schulte**: I mean really, there's just, there's two project tasks on this project Now I know you guys use procore and I think you still do for some projects, Procore, the way that I, I know that they do their, their project tasks.
**Evan.schulte**: What, what happens in our system is when you create a project and you start creating the budget and you push that over and you create, you know, job costs and all that.
**Evan.schulte**: If you're picking a budget code but you're not using a sub job, our system is going to automatically create a project task in Acumatica.
**Evan.schulte**: And the name of that project task is project.
**Evan.schulte**: It's just all uppercase.
**Evan.schulte**: Project.
**Evan.schulte**: Procore does something similar to this, but they use a, an id.
**Evan.schulte**: They use the pro, the project's ID instead of project.
**Evan.schulte**: Now if this job had some sort of connection to procore or something, maybe that it does.
**Evan.schulte**: Yeah.
**Evan.schulte**: So I don't know how that project task even would have gotten created.
**Evan.schulte**: It had to happen at some, you know, at some point during some port from automation that you have or importing expenses from somewhere is where the last call, that's kind of where I, it sounded like they were coming from is some import was being created which had that as the project task.
**Evan.schulte**: Now it wouldn't, it wouldn't have even existed that project task until something created it.
**Evan.schulte**: If you were to, you know, create a new project and push it and everything, it's really, that'll never get created.
**Evan.schulte**: Now you could go to your sub jobs here and you could create a project sub job with a code of 24115 in this case and it will push that over.
**Evan.schulte**: But I don't think you did that or I don't think anybody did that in job plan.
**Evan.schulte**: I, I, in fact, I know it got created on the Acumatica side.
**Evan.schulte**: And the only time anything has been associated with that project task has been expenses that were input into Acumatica.
**Evan.schulte**: And you can see these 10 cost codes were the ones that were brought over with those, those expenses basically.
**Evan.schulte**: So I, I don't know what's causing that to be input.
**Evan.schulte**: I'm, you know, we're happy to work with you guys to, to come to some solution if you don't think that you can stop inputting those into Acumatica.
**Evan.schulte**: But I mean like, obviously, you know, you can, you can use a sub job of a code.
**Evan.schulte**: And I had even suggested on the last car, I didn't suggest this, but I had mentioned, you know, we could even add an option to change how the system works.
**Evan.schulte**: So instead of using project, we used, you know, the ID of the project from Acumatica as the project Tasks default name.
**Evan.schulte**: You know, that's obviously not how this.
**Evan.schulte**: Our system works, but we could add a setting for that or something.
**Evan.schulte**: But you know, there's projects that already use this project task.
**Fnjie**: So let me, let me share my screen here.
**Fnjie**: Let me try to understand this.
**Fnjie**: So.
**Evan.schulte**: Sure.
**Fnjie**: To make sure it would get it right.
**Fnjie**: All right, so I'm in acumatica right here.
**Fnjie**: Okay.
**Fnjie**: So I go to my project tasks.
**Fnjie**: All right, so you're saying this one right here, my task ID is 2411 5, which is that job default.
**Fnjie**: Project task is a description.
**Fnjie**: Project ID is 2411 5.
**Fnjie**: This was created on 4, 8.
**Fnjie**: So this is the correct one.
**Evan.schulte**: No, that is the incorrect one.
**Evan.schulte**: So that's the.
**Evan.schulte**: That is how procore works, I believe.
**Evan.schulte**: And, and I think there's something in your system on the back end that's creating that.
**Evan.schulte**: Our system.
**Fnjie**: So then this one right here, that's is it.
**Fnjie**: Then the 24115 with the project, you're saying that's the correct one.
**Evan.schulte**: Exactly.
**Evan.schulte**: And you notice that that one was created first too.
**Evan.schulte**: So the project was created, it was synced, you created a budget, you did all your costs and everything.
**Evan.schulte**: And then eventually there was an expense that was created for the.
**Evan.schulte**: That project task, which didn't exist yet.
**Evan.schulte**: And it was created by something on the.
**Evan.schulte**: By some process happening outside of Job Planner.
**Evan.schulte**: And.
**Evan.schulte**: Okay, so we're importing that.
**Fnjie**: All right, so this needs to be the setup.
**Fnjie**: The project is the task id.
**Fnjie**: Okay.
**Fnjie**: And then it's the project ID is the number which is the same no matter what.
**Fnjie**: So then that means that all of like these 2,4114, that needs to be deleted.
**Fnjie**: That needs to be deleted.
**Fnjie**: That needs to be deleted.
**Fnjie**: That needs to be deleted.
**Fnjie**: Every single one of these needs to be deleted.
**Fnjie**: Same with these two, Correct?
**Evan.schulte**: Correct, Yep.
**Evan.schulte**: And.
**Evan.schulte**: And I'm just double checking here to make sure that you're looking at the right ones.
**Evan.schulte**: 25 1, 110.
**Evan.schulte**: Yep, you are correct.
**Evan.schulte**: So those need to be deleted.
**Evan.schulte**: And the.
**Evan.schulte**: Yeah, I mean, ultimately the deletion is.
**Evan.schulte**: Is part one, I would say.
**Fnjie**: And I think, well, if we change the status to.
**Fnjie**: To cancel, that would do the trick, right?
**Evan.schulte**: It would probably.
**Evan.schulte**: I think it would probably prevent costs from being imported at least.
**Evan.schulte**: It would.
**Evan.schulte**: It would like error and tell you you can't do that.
**Evan.schulte**: So it would, it would kind of, you know.
**Evan.schulte**: Yeah, I think it would at least prevent any new costs from being associated with it.
**Evan.schulte**: Now you do have costs.
**Evan.schulte**: Like in the, in this Westfield job, you do have costs.
**Evan.schulte**: I Don't know if canceling that right now would prevent you from moving those.
**Fnjie**: We'll move the cost and then.
**Fnjie**: And then cancel it.
**Evan.schulte**: Yeah.
**Fnjie**: Never.
**Evan.schulte**: Yeah.
**Evan.schulte**: So the, the canceling, I, I think is a good option, but there's also the idea, the fact that these were created and, and I think, yeah, moving.
**Fnjie**: Forward, I'm going to be more involved because clearly we don't know what the hell we're doing and figure out some kind of lock to where this doesn't happen, so we don't have to keep doing this.
**Evan.schulte**: Yeah.
**Evan.schulte**: And we.
**Evan.schulte**: The last call that we had had, I can't remember, I think I, I think it was Fatima or somebody had said, you know, the.
**Evan.schulte**: It was imported and they just need to not use that ID as the project task.
**Evan.schulte**: So it sounded like that there was some understanding, at least that there was something happening.
**Fnjie**: When we import it from job pointer, it automatically creates the correct project task, which would be project in this case.
**Evan.schulte**: And it does, it does do that, and automatically.
**Evan.schulte**: And that's why you see that all those, those project versions were created first.
**Evan.schulte**: Those were created like when the project was initially synced, but then somehow, somehow.
**Fnjie**: These other ones are being created.
**Evan.schulte**: Yeah.
**Evan.schulte**: And those.
**Evan.schulte**: And you can even see those were all created on the same day.
**Evan.schulte**: So there was probably some mass import that happened on 4.
**Evan.schulte**: 8.
**Evan.schulte**: And those, all those project tasks were created rather than just using the existing project.
**Evan.schulte**: Project task that was created previously.
**Fnjie**: Yeah, that's exactly what it is.
**Fnjie**: Yeah.
**Evan.schulte**: And so, and so I know we've, like, we've reverted some.
**Evan.schulte**: I mean, we're really fighting the system in a lot of cases because it's like, you know, there's job costs associated with it and our system wants to import them.
**Evan.schulte**: So I know we can get these jobs that already have costs incorrectly associated back.
**Evan.schulte**: You know, just get those costs reassociated or recost, you know, recoded, and we can get them removed from the budget.
**Evan.schulte**: We've.
**Evan.schulte**: We've done that already for the Westfield once.
**Evan.schulte**: And then it sounds like going forward, you know, if you understand it, and I think that will help a lot.
**Evan.schulte**: And it's just that whatever that import is, and I, I don't know how that's being created or what's causing that.
**Evan.schulte**: If it's like a copy, like they get an Excel file and they're just copying one column to another or something.
**Evan.schulte**: Potentially.
**Evan.schulte**: Yeah.
**Fnjie**: I don't know.
**Fnjie**: I'm gonna have to dive into it.
**Jdawson**: Okay.
**Evan.schulte**: If there's anything that, you know, we can do to help, we're we're more than happy to, to assist there.
**Evan.schulte**: Yeah, because we, we obviously want, want that resolved as well.
**Evan.schulte**: Our system is, is ultimately importing these as sub jobs and stuff, which is the way it's supposed to work.
**Evan.schulte**: But I know you want these all in one bucket and so yeah, I.
**Fnjie**: Want the, I want the budget to read.
**Evan.schulte**: Yeah, you basically don't want the 24, 115 and the default project or the default job sub job.
**Evan.schulte**: You want the just all one.
**Evan.schulte**: And if you, if you only have one, you won't even have that sub job header.
**Evan.schulte**: It'll just be one full budget.
**Fnjie**: Just be this one right here.
**Evan.schulte**: Correct.
**Evan.schulte**: Yep, exactly.
**Evan.schulte**: Yep.
**Evan.schulte**: So as long as, as soon as those are reverted, our system is going to import those.
**Evan.schulte**: It's a nightly thing.
**Evan.schulte**: But if, if somebody were to just let us know, hey, these are reverted.
**Evan.schulte**: Now we can even force it to do it.
**Evan.schulte**: I mean, you could do it too.
**Evan.schulte**: But I, I, we're more than happy to help here because then we'll, we'll force it to refresh if you just let us know sooner and then we'll get rid of those budget lines.
**Evan.schulte**: And recoding those is basically so that 24,330, which is currently under that, that incorrect project task will show up underneath of the, the correct project task.
**Evan.schulte**: So that'll just be basically be reallocated under the proper header.
**Fnjie**: So question here.
**Fnjie**: Is there a way.
**Fnjie**: Okay, nevermind.
**Fnjie**: I see how it is.
**Fnjie**: All right, so to get it, so to get a total.
**Fnjie**: All right, general requirements.
**Fnjie**: All right, so it's telling me my total of everything in Division One is the 64, correct?
**Evan.schulte**: Yep.
**Evan.schulte**: Exactly.
**Evan.schulte**: Yep.
**Evan.schulte**: So you should have a, you'll have a total at every level, basically.
**Evan.schulte**: And then at the bottom line, you'll have a total for every sub job and everything included.
**Fnjie**: Got you.
**Fnjie**: Okay.
**Fnjie**: All right.
**Fnjie**: So yeah, so we just need to reclass those and when we reclass them, it'll automatically delete this.
**Evan.schulte**: Or do we need to tell you, Let us know.
**Evan.schulte**: I'll check it.
**Evan.schulte**: So if you, I'll just double check it.
**Evan.schulte**: But if you let us know, we can just do it right away.
**Evan.schulte**: It won't automatically delete the budget lines, but it will zero them out.
**Evan.schulte**: We just need to.
**Evan.schulte**: The system will prevent you from deleting them because there's expenses associated with it, even though they're zeroed.
**Evan.schulte**: So we just need to force it to delete it and then it won't import it again as long as it's a $0amount.
**Evan.schulte**: On Acumatica side which it should be when we delete it.
**Fnjie**: Okay.
**Fnjie**: All right, so I'll dive into this and figure out how to get this fucking shit deleted and make sure it doesn't happen anymore.
**Fnjie**: And so we'll start off by getting everything reclassed so that we aren't running into this issue anymore.
**Jdawson**: Okay?
**Evan.schulte**: Yep.
**Evan.schulte**: Sounds good.
**Evan.schulte**: Like I said, let us know if there's anything we can do to help.
**Fnjie**: Yep.
**Fnjie**: Sorry for wasting your time again.
**Evan.schulte**: No, no, it's not now.
**Evan.schulte**: Wasting.
**Evan.schulte**: We're.
**Evan.schulte**: That's what we're here for, man.
**Fnjie**: All right.
**Fnjie**: Thank you.
**Evan.schulte**: All right, take care, guys.
**Evan.schulte**: Bye.
**Evan.schulte**: Bye.