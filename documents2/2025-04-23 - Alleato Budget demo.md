# Alleato Budget demo
**Meeting ID**: 01JSCPKXP7X12TW8ETK21Q8KQ2
**Date**: 2025-04-23
**Duration**: 113.5 minutes
**Transcript**: [View Transcript](https://app.fireflies.ai/view/01JSCPKXP7X12TW8ETK21Q8KQ2)
**Participants**: evan.schulte@jobplanner.com, gducharme@alleatogroup.com, mcalcetero@alleatogroup.com, bclymer@alleatogroup.com, jmendez@alleatogroup.com, fnjie@thinkplumb.com, ataylor@alleatogroup.com, acannon@alleatogroup.com, njepson@alleatogroup.com, jdawson@alleatogroup.com

## Transcript
**Evan.schulte**: Foreign.
**Gducharme**: So I do have an accepted response from Glenn, Brandon, and Nick, and there was not a response from AJ Or Maria.
**Gducharme**: And I know we said that's not a big deal, but I guess.
**Gducharme**: Do we know for sure if.
**Evan.schulte**: If.
**Gducharme**: Let me message him who else is showing up?
**Gducharme**: Just so you know, if we need to obviously give people a few more minutes, we can do that.
**Gducharme**: I just want to confirm.
**Mcalcetero**: Nick just joined.
**Evan.schulte**: Hey, can you guys hear me?
**Bclymer**: Hi, guys.
**Jmendez**: Yeah, Hi, this is Evan.
**Bclymer**: Hi, Evan, how are you?
**Evan.schulte**: Good.
**Bclymer**: Hi, Christine, how are you?
**Bclymer**: I have a question for you guys.
**Bclymer**: So is there any way that we can record this meeting or can I go ahead and record it here?
**Bclymer**: Because we want to do like an SAP.
**Bclymer**: Do you have a recording?
**Bclymer**: So we want to create it to save it in our future folders and files, so.
**Gducharme**: Oh, yeah, I can absolutely record this now.
**Fnjie**: Awesome.
**Bclymer**: Thank you, Kristen.
**Jmendez**: Awesome.
**Bclymer**: And if you can send it later, I'll appreciate it.
**Gducharme**: I will absolutely do that.
**Bclymer**: Thank you so much.
**Gducharme**: I will wait to start it though, until I know we're all ready to go.
**Bclymer**: I think we are.
**Bclymer**: Brandon is not joining today.
**Bclymer**: Okay.
**Bclymer**: Just so you know.
**Bclymer**: So that's why we will just need the recording.
**Bclymer**: Thank you, Kristen.
**Gducharme**: Sure, I'll get that going.
**Evan.schulte**: All right.
**Jmendez**: It looks like we just got Glenn here.
**Fnjie**: All right, so I'm gonna.
**Fnjie**: I'm gonna go ahead and get started.
**Fnjie**: So my goal today is kind of explain exactly the kind of little.
**Fnjie**: Some little intricacies about how Acumatica and.
**Jmendez**: Job Planner work together.
**Fnjie**: And really there's.
**Jmendez**: There's one specific thing that has been causing some pain on.
**Jmendez**: I know at least two jobs.
**Jmendez**: I.
**Jmendez**: I know of three jobs.
**Jmendez**: There's one that hasn't been mentioned really yet, but I know there's another job that has this on it.
**Fnjie**: So just to maybe summarize it in.
**Jmendez**: Like the simplest way.
**Jmendez**: In.
**Fnjie**: In Job Planner, we have a concept of sub jobs, and in Acumatica you have project tasks.
**Fnjie**: And when you create a project task.
**Jmendez**: Either in Acumatica or a job planner, they're going to synchronize between the two sides.
**Fnjie**: And when you.
**Fnjie**: As far as I can tell, you guys don't use project tasks really to much extent.
**Fnjie**: I know some.
**Jmendez**: Some customers will use them to classify.
**Fnjie**: Different sections of the project.
**Jmendez**: Some will do it by division, and.
**Fnjie**: Some will just do it like you.
**Jmendez**: Do it where they just do a single project task on the job and then that holds all the costs on it.
**Jmendez**: And there's.
**Jmendez**: It's totally fine whichever way you do it.
**Jmendez**: The main thing that you need to know when you do that is when.
**Fnjie**: You push a budget to Acumatica from Job Planner, we're going to create a default project task.
**Fnjie**: So that that project, when you create.
**Jmendez**: It at first, it's not going to have any project tasks on it in Acumatica.
**Fnjie**: And then when you push that budget.
**Jmendez**: From Job Planner to Acumatica, that project task is going to be created.
**Jmendez**: And the project task name is just project.
**Jmendez**: That's the, that's the code for it.
**Fnjie**: And if you look here, we actually.
**Jmendez**: Have two different sections and this is the core of the problem is you have this 2411 Siva Burnville Consulting and then you have this default project task.
**Jmendez**: Now if we go into the cost.
**Fnjie**: Codes, we can see that there's only one sub job and that's because the.
**Jmendez**: Sub job is that 24111.
**Jmendez**: So this is something that was created on the Acumatica side and then costs were associated with it.
**Fnjie**: So my, my goal today is to try to figure out hopefully why these.
**Jmendez**: Are being created on the acumatica side.
**Fnjie**: And make sure that they don't continue to be created.
**Jmendez**: Because ultimately what happens then is when that's created, there's being, there's actual costs associated with it.
**Jmendez**: So if you look at this one, for example, we have an expense travel.
**Fnjie**: Item and there are looks like five.
**Jmendez**: Expenses that are associated with that sub job and all of your other budget items are associ with a different one or project task using the Acumenica terms.
**Fnjie**: So maybe to, to, to boil this.
**Jmendez**: Down to really one thing, it's that we want to make sure that when a project is created in Acumatica at the initial phases of it, if there's being, if there's job costs being entered.
**Fnjie**: In there, we just want to be sure that the task that those are being entered in on is the same.
**Jmendez**: Task that Job Planner is going to be using.
**Jmendez**: There's no difference.
**Jmendez**: So maybe to start out, do you know maybe using 24111 as an example, does anybody know how this project task is being created?
**Jmendez**: I kind of have a suspicion.
**Jmendez**: But I wanted to ask if anybody here knows first.
**Ataylor**: Yeah, hey, I can tell you.
**Ataylor**: So when we, we're used to the project task in Akumatica being the job number because that's what we had in, in Procore.
**Ataylor**: So when we went to upload the credit cards from Notion, the way they were set up, they were set up to use the project task and to use that project task number because of how it was okay in Procore.
**Ataylor**: So Even the Akumatica jobs, we, we had it done like that.
**Ataylor**: So when we went to update to upload the credit card information, we were receiving an error because it did not recognize the project task.
**Ataylor**: So that was my mistake.
**Ataylor**: I went in and I tried to change it and I think it added a new one and that's why it got uploaded as that project task number.
**Ataylor**: So what we did was when we realized the mistake, we went back into Acumatica and we changed the project task on those items back to project and then it moved it to job plan on the project.
**Ataylor**: And that's why on some of them, I think it was on Glenn's job, it later on changed it to zero because it had moved it out of those newly created project tasks into the project.
**Fnjie**: Yes.
**Fnjie**: Yeah.
**Fnjie**: So there's, and, and this, the remediation.
**Jmendez**: Of this has also been another thing that we've kind of been going through.
**Fnjie**: So when, because those, those transactions were.
**Jmendez**: Created, we're, we've pulled in a lot of that stuff.
**Fnjie**: So if you, if you go to the transaction.
**Jmendez**: Let's use one of these for an example.
**Jmendez**: Like this, one of these pay periods here.
**Jmendez**: So these are all associated with two.
**Fnjie**: Well actually no, these, these, this job is actually corrected.
**Jmendez**: Let me go back to the job that has this issue still.
**Jmendez**: So, so we're looking at that one that had those five expenses on the different sub job.
**Jmendez**: And these are still on that, that different sub job on 24111 right now.
**Fnjie**: So what was happening was we were, we were mentioning, hey, these are coded.
**Jmendez**: To the wrong sub job or these are coded the wrong project task using Acumatica terminology.
**Fnjie**: We had said if you recode these to the correct task, those costs will.
**Jmendez**: Be moved over to the correct place.
**Fnjie**: Which did happen.
**Jmendez**: But what I was noticing is that instead of changing the existing expenses in any way, they were being reverted basically.
**Jmendez**: So a new transaction was being created to revert that expense and then another transaction was being created to move the money to a different location, which is totally fine.
**Fnjie**: But the issue that we were having is we were at the same time.
**Jmendez**: We were basically fighting that because what happens is you create that transaction in Acumatica, we pull it into our side and then that populates that cost code and it basically just tells our system, hey, we're using this project task and this cost code together.
**Jmendez**: And so what we were doing is.
**Fnjie**: We were, we were manually removing stuff on our side just to make it, you know, make the budget look the.
**Jmendez**: Way that Glenn wanted.
**Jmendez**: And I think Jose as well and.
**Fnjie**: Then those transactions were being posted to revert and then they were, you know.
**Jmendez**: Hitting the budget on the acumatic or.
**Fnjie**: On the job planner side.
**Jmendez**: We were kind of just fighting back and forth trying to get that.
**Fnjie**: So that's what the purpose of this call was.
**Jmendez**: One to make sure that the there that's resolved in the future.
**Fnjie**: So it sounds like you're importing these from notion.
**Ataylor**: Yes.
**Fnjie**: Right.
**Evan.schulte**: Okay.
**Fnjie**: And, and when you were importing those.
**Jmendez**: You were importing them to the project ID named Project task.
**Fnjie**: And is that something that you're still.
**Jmendez**: Doing or are you now importing to a task name project?
**Ataylor**: Since we caught the error, we haven't made any imports yet.
**Ataylor**: But the next import we need to get with Acumatica because they helped us create the import file.
**Ataylor**: So we are going to work with them to see how they can have it select.
**Ataylor**: What we really needed to select is the project number and then we can manually select the project task as project for the job plan items and the project number for procore.
**Evan.schulte**: Okay.
**Fnjie**: So one thing I was gonna, I was gonna mention but I think.
**Jmendez**: The, the only issue is that you guys have jobs running right now and these jobs are already using this project for terminology.
**Fnjie**: You know, we could, we could add something in place that uses the project ID instead of project.
**Fnjie**: But like I said, all the existing.
**Jmendez**: Stuff that's in, that's in place there is gonna, it's already pointed to that.
**Fnjie**: So if you, if you do have a way to, to do that and we're, we're open to help as well.
**Jmendez**: I mean really the only difference between.
**Fnjie**: How we work in procore works is.
**Jmendez**: Just that task name.
**Fnjie**: It's in procore it's the idea of.
**Jmendez**: The project and in ours it's just capital project, it's just all project.
**Fnjie**: So if there's anything, you know, if you're, if you're importing those and you.
**Jmendez**: And you need us to help or if there's any way that we can help, please reach out to us.
**Fnjie**: But it does sound like at least for the new transaction.
**Jmendez**: So using like 24115 for an example, all the transactions on this job that were for the project ID task have been reverted and moved to the, to the non to the project task basically.
**Fnjie**: And after that was done, we were told about it and we, we went.
**Jmendez**: In here and we basically just removed those budget line items.
**Jmendez**: As long as there's zero dollar line items.
**Fnjie**: So like it if we go back to this project here, the budget is.
**Jmendez**: $0 on this but there's some there's actual costs on here.
**Jmendez**: So we can't just remove this line it from the budget.
**Jmendez**: Ultimately that is what I believe Jose and Glenn want is they want, they just don't want these budget line items showing up.
**Fnjie**: So we can do that on this line as well.
**Jmendez**: We would just need these transactions here to be moved to this project task.
**Jmendez**: And as far as I can tell there's only this project and one other one that has this on it.
**Jmendez**: I can find that other one here.
**Ataylor**: So I think the way Akumatica does it, if we go in to move those, and I believe this is what you were seeing on, on, on Glenn's project when we go in to move those, the only way it can be done in Akumatica is we have to reverse the original.
**Ataylor**: It reverses the original and then recreates it to move it to the right one.
**Ataylor**: So in the original, let's say on like the general requirements now you, you'll see a zero because it'll reverse.
**Evan.schulte**: Will.
**Ataylor**: Add the negatives to net to zero and then move it there.
**Ataylor**: And when we did it on Glenn's job it all showed zero.
**Ataylor**: So I'm not sure why later on it came back on there and it didn't exist.
**Fnjie**: Well, the reason was because we're, we're.
**Jmendez**: Our system wants to show those line items because there's transactions on them.
**Fnjie**: So like if when you create those.
**Jmendez**: Five, if you create those five reversing transactions, there's now 10 transactions on this line.
**Fnjie**: And just by default our system wants.
**Jmendez**: To show those line items.
**Fnjie**: So what we did on our end.
**Jmendez**: Just for this project and the other project is we overrode them to not show those line items.
**Fnjie**: And the expectation was like okay, we're.
**Jmendez**: No more transactions are going to be entered on these lines.
**Jmendez**: So we're safe to set these as just basically just remove them from the budget.
**Jmendez**: But then those new transactions came through which then made it reappear and registered those transactions.
**Fnjie**: So as long as we revert these transactions here and then after those are.
**Jmendez**: Reverted we just hide the line item.
**Fnjie**: Because yeah, you could, you could go.
**Jmendez**: Revert these lines right now that's going.
**Fnjie**: To sink here and this is going.
**Jmendez**: To show $0 both at the actual amount level and on the direct cost they're both going to show $0.
**Fnjie**: But Glenn and, and, or Glenn and Jose, they want it gone.
**Jmendez**: They don't want that line on, on the budget at all.
**Jmendez**: And that's what we were trying to do.
**Fnjie**: So, so yeah, if you can remove those and this shows Zero.
**Fnjie**: We can come in here and we can actually get it rid of it.
**Jmendez**: From the budget and it will.
**Fnjie**: As long as no more transactions are.
**Jmendez**: Created for that line, we're all good.
**Jmendez**: No, it's never going to show up on the budget again.
**Evan.schulte**: Okay.
**Ataylor**: Okay.
**Ataylor**: Sounds.
**Ataylor**: Sounds good.
**Ataylor**: We can do that.
**Evan.schulte**: We'll.
**Ataylor**: We'll just check each job, whatever has cost on those default project tasks will reverse them and then send.
**Ataylor**: Send you a list of what to delete.
**Evan.schulte**: Okay.
**Fnjie**: And I can, I can tell you.
**Jmendez**: Actually I could go really quickly here and I can tell you exactly what jobs have that in it.
**Jmendez**: So I know it's 24109.
**Jmendez**: Okay.
**Jmendez**: And there's.
**Jmendez**: If you want to look at the, the screen here, this shows you the cost codes.
**Jmendez**: It's 013130 and 0165.
**Jmendez**: And there's just, there's two lines there that.
**Fnjie**: So it looks like two of them.
**Jmendez**: Are payroll and then these are travel.
**Evan.schulte**: Travel.
**Ataylor**: Okay.
**Jmendez**: And then the other one is.
**Jmendez**: So there's 24109.
**Jmendez**: The one that we've been talking about is 24111.
**Jmendez**: And that just has those five travel transactions.
**Fnjie**: Westfield is all good.
**Jmendez**: So that, that's what, that's an example of one that we're basically, we're going to do exactly what we did for, for that one to these other two and then we just double check, make sure there's no others here.
**Jmendez**: I think that was the only one.
**Jmendez**: I've already went through these, but I just wanted to make sure.
**Evan.schulte**: Two.
**Evan.schulte**: It's all good.
**Jmendez**: All right, two more.
**Evan.schulte**: That one's good.
**Evan.schulte**: And that one's good.
**Fnjie**: Yep.
**Fnjie**: So just those two.
**Jmendez**: Just 24109.
**Fnjie**: Yeah.
**Fnjie**: So I, and that's kind of what I saw too is I, I had a feeling that I, I know we had talked about this on a project.
**Jmendez**: I think it was one of Brandon's projects back in January.
**Fnjie**: So I thought that going forward this, you know, I thought we had this.
**Jmendez**: Resolved and it seems like we do.
**Fnjie**: It sounds like you guys know exactly.
**Jmendez**: What happen on those.
**Jmendez**: We just need to get these two projects, get those transactions moved and then we'll get those lines just hidden on the budget here and everything should be good.
**Fnjie**: And then going forward, like you were.
**Jmendez**: Saying, you know, getting those notion transactions in when you're importing those, if you, you know, if you need any help doing that, we, you know, just let us know.
**Fnjie**: No, there's obviously things we can do on our end too in terms of.
**Jmendez**: The integration, but because there's already connections on some of the projects there's, you.
**Fnjie**: Know, there's certain things we can and can't do.
**Fnjie**: But we're, you know, we're more than.
**Jmendez**: Happy to work with you guys to, to, to, you know, to make it work.
**Fnjie**: And, and I, you know, this is just kind of a really, we haven't.
**Jmendez**: Dealt with this personally.
**Fnjie**: I think that it seems like this is really a core of like you had a system in place, it worked a specific way with procore.
**Jmendez**: And then you just need to make sure that that workflow works here at Job Planner.
**Jmendez**: And I think we can, I think we can get this all good to go and then moving forward will be good.
**Ataylor**: Okay.
**Fnjie**: All righty.
**Fnjie**: Yep.
**Jmendez**: So 241-09-24111 is cleared out.
**Jmendez**: Any questions from anybody on the call?
**Mcalcetero**: So, and if I missed it, I'm sorry, but.
**Mcalcetero**: So if we come in here and we have some jobs and there's not a cost code for something we need to expense to it do we unlock the budget in Job Planner, add that cost code, block the budget, push it to erp, push the changes and then we're able to to expense in notion the to the right code so it goes to the right code and then we'll acumatica pick that new code up and then does that make everything work out the way it should?
**Fnjie**: You.
**Fnjie**: You don't have to do it that.
**Evan.schulte**: I'm sorry, go ahead.
**Fnjie**: Yeah, so.
**Fnjie**: So you don't have to do that in Job Planner.
**Jmendez**: So Job Planner will synchronize both directions.
**Jmendez**: So if you create the cost code on the project in acumatica for a transaction that's going to pull back into Job Planner, they the only thing you need to make sure of is that that transaction is created on the project task with an idea project and not, you know, the project id.
**Jmendez**: So in this case there's a prod, there's a task with 24111 as as the ID and there's one with just project all capital letters as the ID.
**Fnjie**: If you were to create it on.
**Jmendez**: The 24111 that would be the wrong project task.
**Fnjie**: And that project task really shouldn't even.
**Jmendez**: Exist on most on any of your projects.
**Jmendez**: It just seems like there's two of them I think maybe.
**Fnjie**: Maybe.
**Fnjie**: Well actually three but two of two.
**Jmendez**: Of them that are currently have transactions on them where those tasks were created because of some pre existing automation.
**Jmendez**: In notion from Notion.
**Mcalcetero**: Can you go to the Burnville project?
**Mcalcetero**: I just did that in there and just see if that was correct.
**Fnjie**: Yep.
**Jmendez**: I'm on the Burnville project right now.
**Jmendez**: Here, I'll refresh my page.
**Fnjie**: Okay, so you added a Costco here.
**Mcalcetero**: Yeah, for software.
**Evan.schulte**: Okay.
**Mcalcetero**: Licensing right there.
**Ataylor**: Software licenses.
**Ataylor**: Yeah.
**Evan.schulte**: Yep.
**Jmendez**: So it's right here.
**Mcalcetero**: And I just coded in Notion, that computer that's for Mike or Super there.
**Mcalcetero**: So then I'll just have to do it budget modification to put the money in the.
**Mcalcetero**: Into the right code.
**Evan.schulte**: But.
**Fnjie**: Maybe if you can explain what you're trying to do, I, I don't.
**Jmendez**: Think you should need to do a budget modification.
**Fnjie**: What.
**Fnjie**: What is your.
**Fnjie**: Can you maybe walk through what the.
**Jmendez**: Process that you're talking about real quick?
**Mcalcetero**: So we want to make job costs actual.
**Mcalcetero**: So we can understand at the end of the day how much did we spend and what do we spend it on?
**Mcalcetero**: So like in this case, we have a job that the superintendent needs a computer.
**Mcalcetero**: So that's an actual job cost for that, for that project.
**Mcalcetero**: So I don't want to code it to superintendent expense like that doesn't.
**Mcalcetero**: That's.
**Mcalcetero**: The superintendent's just his labor.
**Mcalcetero**: So the only thing that should be coded to that cost code is labor.
**Mcalcetero**: You know, anything else that comes up on a job, we want to make sure it's got its own code.
**Mcalcetero**: So as long as we're able at that doesn't mess the system up, our PM should go in.
**Mcalcetero**: When they see a cost that doesn't belong in a line that's already there, they just need to create that line and code the expense to that line and then do a budget modification to.
**Mcalcetero**: To cover the cost of that in their job.
**Evan.schulte**: Okay.
**Fnjie**: Yeah, so I kind of follow what you're saying.
**Fnjie**: So if you have it, if you.
**Jmendez**: Had an expense for like in this case, software licensing on the Acumatica side, you would, you would want to code that expense to software licensing to.
**Jmendez**: You're.
**Jmendez**: Is that what you're saying you would do?
**Mcalcetero**: Oh, that's what I, when I coded it in Notion, I put it to.
**Jmendez**: That cost code to the software licensing one.
**Mcalcetero**: Right.
**Mcalcetero**: So the accountant shouldn't have to think at all.
**Mcalcetero**: They should just process it and then it'll charge will come up there.
**Jmendez**: Okay, I understand what you're saying.
**Fnjie**: So you're, you're saying that the.
**Fnjie**: This would base.
**Jmendez**: This would really be for the budget side of things.
**Jmendez**: So.
**Jmendez**: And I'll give you an example.
**Fnjie**: Let's say a transaction comes in on.
**Jmendez**: Through Notion Direct and you know, it gets imported to Acumatica and the PM.
**Fnjie**: Doesn'T have a budget line for software.
**Jmendez**: Licensing or anything in job Planner yet if you create that transaction and jaw in, in Acumatica, that's going to get imported into the job automatically and Pro.
**Fnjie**: And Job Planner so that that creation.
**Jmendez**: Of that line isn't even necessary.
**Jmendez**: If you're creating that transaction on the Acumatica side, it'll just automatically create that line item and then they can do it exactly what you're saying they could.
**Fnjie**: It's going to show up as a.
**Jmendez**: Zero dollar line and then they can do a budget modification for that new cost code that just showed up if they want to cover it, which I believe they're already doing.
**Fnjie**: I think the only problem that they.
**Jmendez**: Were having was that the budget line was on a different section and they were.
**Fnjie**: And, and really it was because they had like two different.
**Jmendez**: So you can see here they have travel and entertainment here and then travel and entertainment here as well.
**Jmendez**: And they wanted to make sure those are consolidated.
**Fnjie**: But I think what you just said.
**Jmendez**: Is exactly what, what the plan is.
**Jmendez**: You.
**Fnjie**: And it can happen.
**Jmendez**: Just maybe mention this.
**Jmendez**: It can happen in any order.
**Jmendez**: So let's say the PM knows that there's going to be a software licensing transaction coming through at some point in the future and they just want to get in here and account for it on their budget before that transaction even hits.
**Jmendez**: They can do that too.
**Jmendez**: So they can come in here, add the line item, move the money to that.
**Jmendez**: They don't even have to push it to Acumatica.
**Jmendez**: It's going to automatically flow.
**Jmendez**: That transaction will flow back, everything will link up.
**Jmendez**: The only reason they would want to push it, I guess I should say, is if you're modifying the budget.
**Jmendez**: So if you do add a line and it, you know, you move money to it, you probably do want to push that so that gets updated in Acumatica.
**Ataylor**: If I may add something for accounting purposes, we would actually prefer it to be done the way Jesse mentioned, because when we push transactions from Acumatica into Job Planner, it gives us an error icon saying that this code is not on the budget.
**Ataylor**: So right now we are using that as a check to get back to the PM and say, hey, we are getting an error on this item.
**Ataylor**: So we would prefer to have the code before we push anything to, you know, Job Planner just in case somebody accidentally coded something to the wrong item.
**Ataylor**: So I would have it done the way Jesse just mentioned.
**Fnjie**: Okay, yeah.
**Fnjie**: And you.
**Fnjie**: And just to clarify, you're saying you get an error when you try to.
**Jmendez**: Import it into Acumatica because the Costco doesn't exist on the project yeah.
**Ataylor**: Will import into Job Planner.
**Ataylor**: But, but it gives us an icon saying hey, this item is not, is not on the budget.
**Ataylor**: If you push it, we will create it.
**Ataylor**: Yes, yes.
**Jmendez**: So you're saying that on purpose.
**Ataylor**: Yes.
**Fnjie**: You're, you're talking about this right here.
**Ataylor**: Yes.
**Ataylor**: So we would prefer to not push anything that is saying hey, this is not in Job Planner.
**Ataylor**: We would prefer to have everything we pushed not give us that, that error.
**Ataylor**: So if they, if the PMs have any transactions in notion that are being coded to work to an item that's not on the budget, we would prefer to have them added on the Job Planner side prior to approving it in notion.
**Evan.schulte**: Okay.
**Fnjie**: And yeah, that's.
**Acannon**: No, Evan, this is.
**Acannon**: Glenn, we, you and I just worked on this to make sure that didn't happen for, for the reasons that we, that we made that happen.
**Acannon**: If it's going to a zero dollar line item, it's because you guys are adding a line item to or a category when it should be an expense.
**Acannon**: You're adding it under equipment or adding it under other or whatever it comes in as.
**Acannon**: And that's not a line item that we had created.
**Acannon**: So it's either labor expense or subcontract.
**Acannon**: There are no other line.
**Acannon**: There are no other categories to code them to.
**Acannon**: But when you guys put them in and it goes under equipment, then it messes, it messes up the budget.
**Acannon**: And when a bunch of transactions happen, we have to, I have to go back and spend hours sending you a list of each time that happens.
**Mcalcetero**: And if you can do a budget modification, Glenn, when you, if you just follow that procedure, when you get an expense come in and you don't have a line to code it to create the line, you can make it whatever kind of cost it is, expense through subcontract and you create that line, you push it to erp, then you go and encode that to it.
**Mcalcetero**: You won't have a problem.
**Mcalcetero**: But you'll also know immediately I need to put money in there instead of it coming in later.
**Mcalcetero**: And then it's just a, a hole in your budget.
**Mcalcetero**: So this way as a pm, you can stay on top of your project and where the money needs to go.
**Acannon**: But, but the point, it's adding it to a category that doesn't exist and it's adding it for no reason.
**Acannon**: If, if it's an expense, put it in expense.
**Acannon**: You put it in, you put it in whatever you want and it shows up.
**Acannon**: And then I have to go in and do a budget modification.
**Acannon**: There's no reason for me to blend.
**Mcalcetero**: You're do that.
**Mcalcetero**: I can stand.
**Mcalcetero**: If you create the budget code.
**Mcalcetero**: I just did it.
**Mcalcetero**: You can select whatever type of cost it is and you create that budget code.
**Mcalcetero**: As long as it's the same thing you're going to code that charge to, it's not going to mess up anything.
**Acannon**: Are you saying something different than what we discussed the other day, Glenn?
**Njepson**: Are you saying if you, if you create your budget and let's say 016 whatever that travel and entertainment right now it's 016500E right.
**Njepson**: It's an expense.
**Njepson**: You're saying sometimes when things are getting coded, when expenses are going over it may be equipment.
**Njepson**: 016500M for material or labor.
**Njepson**: Is that what you're talking about?
**Acannon**: It's been coming in as equipment and there will be a question mark icon saying this Costco didn't exist so we added it and so Now I'll have $0 in the original budget.
**Acannon**: I can do a budget modification.
**Acannon**: But it was, it was also doubling them up on the committed and direct cost.
**Evan.schulte**: It.
**Acannon**: It wasn't.
**Acannon**: Yes, it was doubling up.
**Njepson**: Yeah.
**Njepson**: It could have just been a mistake and they, you know accounting can go back and just change that, that line item to the proper Costco.
**Njepson**: But it happens.
**Acannon**: Right, but that my.
**Acannon**: Why, why would we go back and why would we have to go back and change it instead of just coding it to the expense or the category it's there in the first place saying.
**Njepson**: Glenn, they made a.
**Njepson**: They may have made a mistake in.
**Acannon**: Which people make mistakes.
**Ataylor**: So, so they were.
**Ataylor**: And so we enter, when we enter transactions, we don't get to select whether it goes to expense or a sub.
**Ataylor**: What happens is just like Jesse was saying, if the code is already on the budget, it will go to whatever you have it as if it's not on the budget.
**Ataylor**: I think Akumatica just will pick expense or equipment to put that to.
**Ataylor**: We don't select that it is on the.
**Acannon**: But Evan, wasn't that.
**Acannon**: Didn't you call it like the inventory list?
**Acannon**: That's where they get it in Acumatica to, to put it towards expense equipment, material, etc.
**Fnjie**: Yeah.
**Fnjie**: So there, there was.
**Fnjie**: I think that there might be some.
**Jmendez**: Confusion here Glenn because there was a.
**Fnjie**: There's a configuration in here and I.
**Jmendez**: I can actually show you this here really quick.
**Jmendez**: So when we import costs from Acumatica, for example, when, when, when an expense is imported, it's actually mapped to something called a non stock item in Acumatica.
**Jmendez**: And this is what ultimately gets selected on those expenses.
**Jmendez**: And so what this was set up as previously as this was mapped to a different one than others.
**Jmendez**: So when transactions of other were coming in, those were getting mapped to.
**Jmendez**: I believe it was equipment because it's the first one in the list.
**Jmendez**: So basically what it was doing was we were getting transactions that were mapped to other and the system is looking what cost type does this map to.
**Jmendez**: And it wasn't finding anything.
**Jmendez**: So it was just, it was picking the first one so it could properly bring that cost in at least.
**Fnjie**: So we went in here, we just.
**Jmendez**: Made sure that all these cost types here have the correct mapping.
**Jmendez**: And really it was only this expense one that wasn't mapped to the other one.
**Jmendez**: So we fixed that one and then we just, we just resolved those transactions.
**Fnjie**: So I think that might be, that, that might be like just the confusion here.
**Fnjie**: I.
**Fnjie**: That was, that was something that was.
**Jmendez**: Just a configuration and we, we fixed it, we resynced it, and everything's good to go for that one.
**Fnjie**: And, and like, and you were so you.
**Jmendez**: But you are 100, right?
**Jmendez**: Those were being imported and you did have that budget line correctly on there.
**Jmendez**: So, Glenn, doubling the costs too?
**Acannon**: It was doubling, yes.
**Jmendez**: Yeah.
**Fnjie**: And there's, and that's, and that's why this, this problem is.
**Jmendez**: I think this deserved a call because it was hard to do over email because really there were two different ones.
**Fnjie**: And there was the, the cost type.
**Jmendez**: Thing, which was just a configuration thing.
**Jmendez**: We got that all fixed.
**Jmendez**: Everything got imported properly and, and there's no persisting issue or, you know, issue that we need to fix for that anymore.
**Jmendez**: That's all good to go.
**Jmendez**: It's really only this project task one now, and it sounds like we have a resolution for that.
**Jmendez**: We just need to get those moved.
**Jmendez**: We'll get this cleared off going forward.
**Fnjie**: You're gonna make sure that.
**Jmendez**: And you're, and you're already doing this, by the way.
**Jmendez**: I, I'm almost 100 sure you're already doing exactly what we were talking about here, where you, you have those lines on the budget.
**Jmendez**: So an expense comes in, you already have that line on the budget and you did for these travel ones.
**Jmendez**: So you had the travel expense in there.
**Jmendez**: And so as long as we follow this, this what we're talking about, everything I think will be go.
**Evan.schulte**: Will go good.
**Acannon**: The default project task came up on the Westfield Collective project too, but you guys fixed it, took it off, and then it came back.
**Acannon**: It's.
**Acannon**: It's currently off.
**Acannon**: But I was getting them doubled up there too.
**Acannon**: But it's not like that in my job anymore.
**Evan.schulte**: Is this.
**Fnjie**: Yep.
**Acannon**: Yeah, it's gone now.
**Fnjie**: Yep.
**Fnjie**: So that's what we're.
**Fnjie**: We were talking about where we had cleared that out.
**Jmendez**: Basically we're doing some manual effort on our end just to make these projects not have those lines.
**Jmendez**: We're basically fighting what our system wants to do.
**Jmendez**: Our system really wants to show those lines because they have transactions on them.
**Jmendez**: Even though the line is $0, there are a bunch of transactions behind it.
**Jmendez**: So our system's like, well, you know, there's things here we shouldn't be.
**Jmendez**: You know, this budget line should be on here.
**Fnjie**: So we got rid of that.
**Jmendez**: But then some of those reverting transactions hit, so our system wanted to add the line back.
**Jmendez**: So we were kind of just fighting that.
**Fnjie**: But the, the Westfield Collective one, all.
**Jmendez**: The transactions have been moved to the proper project task and yeah, we know no more transactions are going to come on for that other project task.
**Fnjie**: We've got this budget properly.
**Jmendez**: We've got that line removed from the budget at that zero dollar line.
**Fnjie**: So I, we're confident that Westfield Collective is exactly where it needs to be.
**Fnjie**: And what we're really talking about now is making sure that the Burnville one.
**Jmendez**: And then the, the other one was 24109, the Goodwill Bloomington ones just have the same exact thing done to them.
**Jmendez**: We move those transactions to the, to the other project task.
**Jmendez**: We get rid of those lines on there on this budget and then going forward, you know, no transactions are going to be created on this other project task.
**Jmendez**: So, you know, this issue won't come up again.
**Fnjie**: All righty.
**Fnjie**: Any.
**Jmendez**: Sorry, go ahead.
**Njepson**: No, I was just going to ask.
**Njepson**: I had mentioned in a couple emails that there is no revenue option.
**Njepson**: Jesse, do you want to keep having these things as far as our unallocated costs in our, you know, profit and all that, do you want that still going to an expense line item or a revenue line on?
**Njepson**: Because I know in Acumatica there is a revenue option when you're billing the, the owner.
**Mcalcetero**: Whether we do both codes that we would never code anything to.
**Mcalcetero**: So I don't really care what it's called.
**Mcalcetero**: There are lines that, you know, money can go in and out.
**Mcalcetero**: Excuse me.
**Mcalcetero**: Unallocated cost, but no cost should ever be charged to that.
**Fnjie**: Right.
**Evan.schulte**: Okay.
**Fnjie**: Yeah.
**Fnjie**: So we've got.
**Fnjie**: I, I'm not sure if this is what you're talking about.
**Fnjie**: We did have a, an item come.
**Jmendez**: In last week where we were talking about the revenue item that's used when it, when it pushes Acumatica for receivable invoices.
**Jmendez**: Is that what you're referring to?
**Njepson**: I.
**Njepson**: I was referring to when we build our budget.
**Njepson**: We.
**Njepson**: We have a budget line item for contractor fee, let's say.
**Njepson**: And right now that Costco type is an expense.
**Njepson**: There's no option really.
**Njepson**: It's revenue.
**Njepson**: But it's.
**Njepson**: Jesse's right.
**Njepson**: If we're not charging anything to it, we should be fine.
**Mcalcetero**: And fatigue.
**Mcalcetero**: Is there, Is there any accounting reason that if you were doing an audit or anything else that if that was called revenue versus expense, does that really matter to you?
**Ataylor**: Yes, it does.
**Ataylor**: And I was going to bring up the revenue items.
**Ataylor**: We noticed that on in Job Planner, the revenue.
**Ataylor**: The revenue budget is there, the detail is there.
**Ataylor**: But when it comes over to Acumatica, it just syncs us one line item and we were having trouble syncing one revenue invoice.
**Ataylor**: Fritzi, what was that, that job.
**Ataylor**: What job was that on?
**Jdawson**: I think that was Aspire.
**Jdawson**: The Vorh.
**Ataylor**: Aspire.
**Jdawson**: Yeah.
**Jdawson**: Actually it was synced from.
**Jdawson**: There's an option that we can sync from Job Planner.
**Jdawson**: It's the revenue.
**Jdawson**: I believe in Procore what we are doing is we manually entered the owner's bidding from.
**Jdawson**: You sent us the invoice from Pocorite and we manually entered it in automatic.
**Jdawson**: But in Job Planner we have that option that we can sync the revenue from Job Planner to Procore to Automatica.
**Jdawson**: But what happened is instead of a revenue item, it's an expense item.
**Fnjie**: Yes.
**Fnjie**: And we got that fixed.
**Jmendez**: So in.
**Jmendez**: I'm going to show you.
**Njepson**: Yeah, there it is.
**Njepson**: Setting 550500 is an expense.
**Evan.schulte**: All right, so let me just.
**Jmendez**: I'm on my.
**Jmendez**: My system here just to show you these settings here really quick.
**Fnjie**: So in your acumatica settings, we.
**Fnjie**: And this is all set up for.
**Jmendez**: You already, so you don't need to do anything here.
**Fnjie**: But last.
**Fnjie**: I think it was.
**Fnjie**: I think it was not last week.
**Jmendez**: But the week before we had added a feature where we now have the revenue non stock item selectable here as a separate item.
**Jmendez**: So when we push receivable invoices, this is the non stock item that we use.
**Jmendez**: Yours is set up as revenue.
**Jmendez**: Now there was a.
**Jmendez**: There was a weird.
**Fnjie**: I don't know exactly what happened last week.
**Fnjie**: Somebody.
**Fnjie**: Somebody seemed to edit the item after it was set.
**Jmendez**: We had set it to revenue and then it got changed back or it got changed to something else.
**Jmendez**: It was like auto.
**Jmendez**: Some auto exp.
**Jmendez**: I Think it was at one point, but we went back in there, we changed it back to revenue and everything.
**Jmendez**: Everything's still revenue as far as I can tell.
**Jmendez**: So, yeah, any receivable line items that are pushed or the.
**Jmendez**: Anything, you know, after that was set basically will have the revenue account group rather than the expense that you were seeing before.
**Jmendez**: But somebody had mentioned a single line.
**Jmendez**: Can, can you elaborate on that part?
**Ataylor**: Yeah, pulling up the.
**Ataylor**: Can you pull up the revenue budget for Aspire on.
**Ataylor**: In.
**Ataylor**: In Job Planner?
**Fnjie**: I can't.
**Fnjie**: I can pull up the related contract here so I can go.
**Jmendez**: I could.
**Jmendez**: I gotta go to the right system.
**Evan.schulte**: Here so I can go to the.
**Jmendez**: Contract which is related to the revenue budget.
**Jmendez**: So in this case we've got.
**Jmendez**: Which aspiring.
**Mcalcetero**: Was it Fatima?
**Ataylor**: I think.
**Ataylor**: Was it Daytona?
**Ataylor**: I think it was Daytona, yeah.
**Evan.schulte**: Okay.
**Jmendez**: All right, so.
**Fnjie**: All right, so it looks like this.
**Jmendez**: One doesn't have a revenue budget or a contract created on it yet.
**Ataylor**: Okay, then it was the previous one.
**Jmendez**: Okay, so it's probably Ridge then.
**Jmendez**: Ridge, Haven, St.
**Jmendez**: Lucie.
**Ataylor**: St.
**Ataylor**: Lucie 25, 102.
**Evan.schulte**: Okay, so it looks like this one has a.
**Jmendez**: Okay, so nine items and then one invoice has been pushed for this so far.
**Jmendez**: And I'm guessing this is probably one that based.
**Jmendez**: Just based on the.
**Jmendez**: The date that it was created.
**Jmendez**: This is probably one that was pushed before we had added that setting for.
**Fnjie**: The revenue so that any in that.
**Jmendez**: Invoice was likely created with the expense lines.
**Jmendez**: But when that invoice is pushed, it's going to push it based on how your Acumatica project is set up.
**Jmendez**: So the revenue budget level, if it's.
**Fnjie**: At a task level, that that invoice.
**Jmendez**: Will have a single line on it.
**Jmendez**: Well, it'll have one line per task.
**Jmendez**: Basically that's being billed.
**Jmendez**: And if you have the revenue budget at the tasks and cost code level in Acumatica, it'll.
**Jmendez**: It'll do it at the Costco level.
**Jmendez**: So we're always sending the Costco to Acumatica.
**Fnjie**: It's just a matter of if you.
**Jmendez**: Have that level enabled on the project and that'll basically determine what you're billing on the Acumatica side does.
**Ataylor**: Okay, because I want us to start, I want us to be able to sync the AR items from Job Planner into Acumatica.
**Ataylor**: That way we make sure that everything is exactly the way it needs to be.
**Ataylor**: My only concern is that in Acumatica right now, I don't think we have it activated on the Costco level.
**Ataylor**: It's just one line.
**Ataylor**: Items One line item in Acumatica.
**Fnjie**: Yeah.
**Fnjie**: And that in terms of like functionality, that's fine.
**Fnjie**: I mean, if that's not what you.
**Jmendez**: Wanted to do, that's totally fine too.
**Fnjie**: If you could change it, however, you.
**Jmendez**: Can move it and change it to the task and Costco level, but it will work at just a task level too.
**Jmendez**: So if I like in this case, this invoice that was created here in Acumatica will just have one task.
**Jmendez**: Basically, it'll just have a single task on it instead of having every Costco on it.
**Jmendez**: So it works at both levels.
**Jmendez**: But if you do want to bill at the task and Costco level on the Acumatica side, then yeah, you would want to change it on that side too to make sure that, you know your revenue.
**Jmendez**: It's going to affect two things, right?
**Jmendez**: It's going to affect your, your revenue budget will show up at a Costco.
**Fnjie**: Level if you do that too.
**Jmendez**: And the, the contract will sync to that as well.
**Jmendez**: So like this contract here, for example, in Job Planner has nine line items on it.
**Jmendez**: When we push this to Acumatica, we push nine separate line items with the, the project task, the cost code, the account group, all that separately.
**Jmendez**: But Acumatica internally just rolls it up to the task level if you have that enabled.
**Jmendez**: So really there's nothing, there's nothing you need to change in terms of the integration.
**Jmendez**: You just need to decide when you want to.
**Jmendez**: If you do want to change that revenue budget level and you can do that at a single project, you know, you could just do that for one project.
**Jmendez**: You could do it for all your projects.
**Jmendez**: That's totally up to you.
**Ataylor**: Okay, so if we have it, and this may be a Cometica question, if we have a, let's say we have an invoice, we, let's say Jesse wants to send an AR invoice to a customer that we want to print out Acumatica, are we going to be able to see what line item is being invoiced or is it going to be lumped into one and just show, let's say $11,000 issued on this project.
**Fnjie**: So in this case, like, for this invoice, this will show it's.
**Jmendez**: It's all based on the project in Acumatica.
**Jmendez**: So if the revenue budget level has a.
**Fnjie**: And I'm actually going to check, I.
**Jmendez**: I'm kind of talking based on what I, I believe it does.
**Jmendez**: I'm pretty sure it's just going to be a single line when it's a task level.
**Jmendez**: So, like in this case, this, this project and likely I believe all your projects are, are.
**Jmendez**: Have a revenue budget at a task level.
**Jmendez**: Right.
**Jmendez**: Not a test and Costco level.
**Evan.schulte**: If.
**Jmendez**: Do you know if that's correct?
**Ataylor**: Yeah, I think it's just a revenue on a task right now.
**Fnjie**: Okay, so in that, in that case we will.
**Fnjie**: It actually.
**Jmendez**: Okay, so just checking something.
**Fnjie**: Okay, actually I.
**Jmendez**: I think I'm wrong about that now that I look at it.
**Fnjie**: I'm just looking at acumatica here.
**Jmendez**: Let me just check to see.
**Jmendez**: I'm looking at one of my.
**Jmendez**: I'll bring over my acumatica system here.
**Jmendez**: So this is a, this is an invoice that was pushed.
**Jmendez**: A receivable invoice that was pushed and you know, the inventory idea is material.
**Fnjie**: You, I.
**Jmendez**: That you can ignore that.
**Jmendez**: I selected material just like you have revenue selected.
**Jmendez**: I had, I had material selected for the, the inventory id.
**Jmendez**: But the.
**Jmendez**: I'm just going to check this project here.
**Jmendez**: I think this project is at a task level.
**Jmendez**: So just verify.
**Fnjie**: No.
**Fnjie**: Okay, so here you can see this.
**Jmendez**: Project is at a task and Costco.
**Fnjie**: Level for the revenue budget.
**Jmendez**: So the revenue budget has the project task and the cost code on it.
**Jmendez**: And then on the invoice side, this invoice was created and it has both the project task and the Costco.
**Jmendez**: So in this case it has, you know, six line items.
**Jmendez**: Now if this didn't have.
**Jmendez**: Let me see if I have an example of just one that has.
**Jmendez**: Okay, so this one has a cost code.
**Fnjie**: You know what, it might actually, this is some.
**Fnjie**: This is something I don't 100% know.
**Fnjie**: So let me just see.
**Jmendez**: It might always do the Costco level at the billing side and I might be wrong about that.
**Fnjie**: I mean we always push the Costco with the billing.
**Jmendez**: The question is, does Acumatica show it?
**Fnjie**: Okay, they do.
**Ataylor**: I'm looking at Aspire right now and the revenue budget is on the task level.
**Ataylor**: The cost is on the task and the cost code level.
**Ataylor**: But the revenue budget is just on the task level.
**Fnjie**: Yeah, but what about that invoice that was created?
**Fnjie**: So this, this invoice that we were.
**Jmendez**: Looking at here for this 37.224.80 that was created for Aspire.
**Jmendez**: Does that have nine line items on it?
**Jdawson**: Yes, previously, but I just deleted.
**Jdawson**: I wanted to resync it so that we would know what are the changes made of that as what you have mentioned.
**Jdawson**: What was sync last time was before the correction.
**Jdawson**: Right?
**Fnjie**: Right.
**Jmendez**: Yeah.
**Jdawson**: And link it and then link to.
**Fnjie**: ERP and then yeah, absolutely.
**Fnjie**: So you want me to unlink this and re.
**Jmendez**: Push it?
**Jdawson**: Yes, so that we would know.
**Fnjie**: Yep.
**Fnjie**: So.
**Fnjie**: So this invoice, just.
**Jmendez**: Just to make sure I'm.
**Jmendez**: I'm understanding correct this Saint Aspire at Saint Lucie invoice receivable invoice number one.
**Jmendez**: You want me to unlink it and then push it again to Acumatica?
**Jdawson**: Yes, please.
**Evan.schulte**: Okay.
**Jmendez**: Whoops.
**Evan.schulte**: Click push again.
**Jmendez**: And go ahead and approve that.
**Jmendez**: All right, so you should see a new invoice in there similar to this one here, where I believe, based on what I'm seeing, it should have the line items broken out by Costco.
**Fnjie**: We definitely pushed.
**Jdawson**: The inventory.
**Jdawson**: ID is still auto expense.
**Fnjie**: You're what?
**Evan.schulte**: Something.
**Jmendez**: All right, let me just look at this really quick here.
**Jmendez**: One second.
**Fnjie**: I can.
**Jmendez**: Can you delete that invoice?
**Jmendez**: We'll just re.
**Jmendez**: Push it.
**Jmendez**: Seems like that got reset for some reason.
**Jmendez**: I gotta go to the right invoice or I gotta go to the right project here.
**Evan.schulte**: Spire.
**Jmendez**: All right, let me go ahead and.
**Evan.schulte**: Unlink.
**Evan.schulte**: Push.
**Evan.schulte**: Let me just do this here.
**Jmendez**: All right.
**Evan.schulte**: Just one second.
**Jmendez**: I gotta update the integration here.
**Jmendez**: All right, so if I go to here.
**Jmendez**: Yeah, it did get switched.
**Jmendez**: That's weird.
**Fnjie**: Just to make sure nobody.
**Fnjie**: Nobody switched this.
**Evan.schulte**: Here.
**Jmendez**: This default revenue non stock item.
**Jmendez**: I'm guessing nobody did.
**Fnjie**: I'll look at.
**Evan.schulte**: Okay.
**Jmendez**: I'll look at why that got switched again.
**Jmendez**: So I'm going to change this to revenue.
**Jmendez**: Go ahead and change it.
**Jmendez**: So now we can see it's revenue.
**Jmendez**: Just verify.
**Evan.schulte**: Yep.
**Jmendez**: So it's revenue.
**Jmendez**: All right, so I'm going to go ahead and approve that receivable invoice now.
**Jmendez**: You ready for me to go ahead and push that again?
**Ataylor**: Yeah.
**Evan.schulte**: Okay.
**Jmendez**: Okay, you want to go ahead and check that one now?
**Jmendez**: And I'm going to go and make sure that this didn't get switched back for some reason.
**Jmendez**: No, we're good to go.
**Fnjie**: Yeah, we'll.
**Jmendez**: We'll look at that and see why.
**Ataylor**: Yeah, it says revenue now.
**Evan.schulte**: Okay.
**Jmendez**: Yeah, I'm going to write this down just for me to investigate to see why that switch.
**Fnjie**: We actually, we released a change this.
**Jmendez**: Weekend that adds a level of permission.
**Fnjie**: There was a.
**Jmendez**: There's basically a brand new permission that you would have to have to manage integrations.
**Fnjie**: So we, we.
**Jmendez**: We know that nobody's editing it now.
**Jmendez**: We're pretty confident that nobody edited that.
**Jmendez**: So yeah, we'll.
**Jmendez**: We'll look into that and see why that got switched over to subexp Revenue.
**Evan.schulte**: Getting switched.
**Ataylor**: I do have another question.
**Fnjie**: Yeah.
**Ataylor**: What's up when we go.
**Ataylor**: I went in to try to pretend like I'm printing the invoice.
**Ataylor**: All it says is just revenue.
**Ataylor**: So, Jesse.
**Ataylor**: So, Jesse, on those.
**Ataylor**: Let's say we are submitting an invoice.
**Ataylor**: Do you, do you want the detail of the line item being built on the invoice, or are you okay with just.
**Ataylor**: It's saying revenue?
**Mcalcetero**: Well, it should be.
**Mcalcetero**: I mean, unless we're attaching a pay application to it.
**Mcalcetero**: And some of them, some of our clients don't require.
**Mcalcetero**: Would be better if the invoice had like one for general conditions.
**Ataylor**: Yeah.
**Mcalcetero**: And then one for each, like, main line on our budget, like how much we're billing to that.
**Mcalcetero**: It just helps know where we're at.
**Ataylor**: Okay, Evan, question too.
**Fnjie**: Yep, I see that.
**Fnjie**: So just before that.
**Fnjie**: So you guys.
**Fnjie**: Yeah.
**Fnjie**: So if you're generating it out of.
**Jmendez**: Acumatica, that'll ultimately be controlled by Acumatica.
**Jmendez**: We are putting it in the Costco.
**Fnjie**: If you, if you find that, like.
**Jmendez**: There'S some, you know, value that you want filled in that we're not currently filling in, please let us know.
**Jmendez**: We're very open to making changes like that.
**Jmendez**: But we do put the cost code, the account group, and then I believe the description.
**Jmendez**: I have to double check on the invoice if there even is a description field.
**Jmendez**: But we, we will pull that over if there is.
**Jmendez**: And then I just wanted to mention too, we do have an export as well.
**Jmendez**: So some, some people use ours, some people go directly through Acumatica.
**Jmendez**: That workflow is really flexible.
**Evan.schulte**: I'll.
**Jmendez**: You know, just as one example, we have a customer, multiple customers, who they generate the invoice, the receivable invoice.
**Jmendez**: They send it out, they get it approved from their customer, and then once that approval takes place, that's when they push it to Acumatica.
**Jmendez**: So basically, once it makes it way in Acumatica, it has been approved.
**Fnjie**: But like I said, that, that workflow.
**Jmendez**: Is totally up to you.
**Jmendez**: So if you want to push it to Acumatica and handle it from there, that is no problem.
**Jmendez**: Glenn, I see you got the, the hand up button press there.
**Fnjie**: What's up?
**Jmendez**: He's just way muted by the.
**Acannon**: Yeah, AJ was in here trying to help me out with something.
**Acannon**: All right.
**Acannon**: Yeah, I, I missed the last 10 minutes.
**Acannon**: He was in here asking me some questions.
**Acannon**: I, I have an issue with a project that I don't.
**Acannon**: I guess I don't know the process when I create a new job.
**Acannon**: We had a job go from estimate into, you Know we want it, and now we have a job number for it.
**Mcalcetero**: I've created the project for all that with you, Glenn.
**Mcalcetero**: That's not really.
**Mcalcetero**: I can go over all that with you.
**Acannon**: Yeah.
**Acannon**: Okay.
**Mcalcetero**: So.
**Acannon**: All right, well, I can't.
**Acannon**: I just.
**Acannon**: I can't link it to ERP or anything.
**Acannon**: I don't.
**Acannon**: I wrote the commitment.
**Acannon**: I can't connect anything.
**Acannon**: Is that something you can do?
**Evan.schulte**: Or.
**Acannon**: I mean, I got Acumatica and job planner here.
**Evan.schulte**: Which.
**Fnjie**: Which job is it, Glenn?
**Acannon**: Goodwill foundations.
**Evan.schulte**: Goodwill Foundations, 25111.
**Acannon**: Yeah.
**Fnjie**: Okay, so it looks like it's pushed to ERP.
**Jmendez**: It's just waiting to be approved here.
**Evan.schulte**: Do you.
**Jmendez**: Let me just see if that's already in there.
**Evan.schulte**: Doesn't look like it.
**Jmendez**: Let me just refresh and make sure.
**Acannon**: So I'm also kind of confused on.
**Acannon**: On what.
**Acannon**: What the ERP admin, because I get.
**Acannon**: You got to go in and, you know, approve the vendor, export the vendor, and then approve the commitment.
**Acannon**: What is projects?
**Fnjie**: Yeah.
**Fnjie**: So on that Goodwill project, before you.
**Jmendez**: Can even push a commitment, the project has to be linked, which you did push the project.
**Jmendez**: It just has to be approved.
**Jmendez**: It flows through the ERP admin.
**Jmendez**: So if you look at my screen here, I'm actually showing that ERP admin page.
**Jmendez**: So in ERP admin, projects ready to export, you've got that Goodwill Foundations project here waiting to be approved.
**Jmendez**: So the process is really simple for this.
**Jmendez**: And the same goes for commitments.
**Jmendez**: And really everything you click approve.
**Jmendez**: And then for acumatic, in this case, you just have to give it a project ID.
**Jmendez**: So that would be 25111 for you guys.
**Jmendez**: And this will create it.
**Njepson**: That's the step I just missed.
**Njepson**: I didn't know you had ERP admin on your thing.
**Njepson**: So you can go ahead and just shoot it over yourself once you create the job.
**Acannon**: That's my.
**Acannon**: That is my next question.
**Acannon**: So I.
**Acannon**: I can access this on my.
**Acannon**: On my end.
**Njepson**: I'll come over and look.
**Evan.schulte**: One second.
**Acannon**: No, I can't.
**Acannon**: I tried to pull this up, and I.
**Acannon**: I don't have access to that job on projects.
**Jmendez**: So on your sidebar, it should.
**Fnjie**: You should have access.
**Evan.schulte**: Yeah, you have access.
**Njepson**: You're ready to export.
**Evan.schulte**: Okay.
**Njepson**: But then if you just enter the 25, 111, then it'll be over.
**Evan.schulte**: You'll be good.
**Jmendez**: I don't think there's any dash in.
**Evan.schulte**: It if I'm looking right.
**Jmendez**: Maybe there is.
**Jmendez**: You would know better.
**Jmendez**: But I think in your.
**Acannon**: Yeah, yeah.
**Jmendez**: I think an acumatic is just 2 5, 1 1.
**Acannon**: I missed that step.
**Acannon**: Yeah, well that's, that's not the only one.
**Acannon**: I.
**Acannon**: I can't.
**Acannon**: I can't do both.
**Acannon**: I can't do both.
**Acannon**: I got all these people on here.
**Acannon**: I'm gonna ask them through here.
**Jdawson**: Okay, so Project ID Nakomatica has a dash.
**Fnjie**: What's that?
**Jdawson**: Project ID Nakomatica has E.
**Jdawson**: Oh, it.
**Jmendez**: Does have a dash in it.
**Jmendez**: Okay, we can fix that if it's already.
**Jmendez**: Has it already been pushed?
**Acannon**: Yeah, so I just did.
**Acannon**: I just did it and pushed it or exported it.
**Jdawson**: Yeah.
**Acannon**: So.
**Evan.schulte**: Okay, let me see if it's in the import list.
**Acannon**: I don't know where it goes because.
**Mcalcetero**: The commit one thing on here before.
**Mcalcetero**: I know you had to write a commitment but like now we're going to do a change order because the budget amount.
**Ataylor**: It says active in acumatica.
**Ataylor**: Now it was in planning before, now it's active.
**Evan.schulte**: Okay.
**Ataylor**: But there is no customer id.
**Ataylor**: Not sure if that came from job planner.
**Jmendez**: No, that's the description.
**Acannon**: Hold on.
**Acannon**: There's no one.
**Jdawson**: It should be added.
**Ataylor**: It should be added.
**Evan.schulte**: Okay.
**Jdawson**: Yeah.
**Acannon**: So guys, I.
**Acannon**: I haven't been shown this process yet, so I need.
**Acannon**: I'm going to take the opportunity to ask this questions and learn.
**Acannon**: I'm sorry, but I haven't.
**Acannon**: I just haven't been shown this process on how to get this stuff in here.
**Acannon**: And I'm trying to ask the questions of the things that are.
**Acannon**: Are the blanks that I need to fill in the specific parts of the process that don't make sense to me or I can't get right now.
**Acannon**: You see you have an option to push to ERP right there.
**Acannon**: I do not have that option on my, on my end for the subcontract.
**Acannon**: I can't push to erp.
**Jmendez**: Can you share your screen?
**Acannon**: Yeah.
**Jmendez**: Okay, go ahead and click into that subcontract.
**Acannon**: There it is.
**Fnjie**: I'm guessing you.
**Jmendez**: It was before the project had been pushed.
**Fnjie**: Like if you had this tab open.
**Jmendez**: Or something and you pushed it on a different tab, you just had to refresh the page.
**Acannon**: Yeah, but.
**Jmendez**: Yeah, so now, so now the project is pushed.
**Jmendez**: There really there's three requirements.
**Jmendez**: One, the project is pushed to the vendor is linked and then three, the commitment you're trying to push has line items on it.
**Evan.schulte**: Okay.
**Acannon**: I've never had to do this.
**Acannon**: Well, I guess this is the first new project that I built because Jesse already had the other west build in here.
**Acannon**: So create the project, go in here, export it.
**Acannon**: Now the vendors, here's.
**Acannon**: And here's one that I'm curious about because we'll go say ready to export.
**Acannon**: There's one of mine.
**Acannon**: Here's a where vendor id.
**Acannon**: I didn't have any answer for this, so what I've been putting in is see here's Merit.
**Acannon**: This has been their vendor id.
**Jmendez**: Yeah, that's probably not a good one to use.
**Jmendez**: The vendor ID is really just an identifier that Acumatica uses.
**Jmendez**: When you create a vendor in Acumatica, I think it might automatically assign it in some cases, but basically it's just a.
**Jmendez**: An id.
**Fnjie**: So like you could do merit M.
**Jmendez**: E R I T T C O N or so, you know, M E R con.
**Fnjie**: It's kind of just like an abbreviation.
**Jmendez**: Like an identifier for this person.
**Fnjie**: It's not unless you guys have like.
**Jmendez**: A set in stone.
**Fnjie**: This is what we always do.
**Jmendez**: Usually customers and just kind of free form that they look at the company name and they just decide, you know, the vendor ID should be M E R C O N T.
**Jmendez**: For Merit Contracting, for example, does this apply now.
**Acannon**: That say we added vendors, this going to carry on to all of our projects in the future?
**Fnjie**: Yep.
**Acannon**: These dumb numbers I've given them will be their vendor id.
**Fnjie**: Yes, they can be, I mean they can be changed.
**Fnjie**: Yeah, we, we can change them and we can.
**Jmendez**: One, we can change them or two, we can unlink and re.
**Jmendez**: Push them.
**Jmendez**: But yeah, the numbers that you use will be their, their value.
**Ataylor**: If, if I may chime in there, I think what that did is created a new vendor for Merit when we already had Merit.
**Ataylor**: So keeps happening.
**Ataylor**: Yeah.
**Ataylor**: When you have a subcontract, just ask one of us.
**Ataylor**: We'll give you the vendor ID from that way.
**Ataylor**: You just input it.
**Acannon**: Hold on.
**Acannon**: It's because when you have say I4 contacts for CNC Foundations, if I, if I push them all to erp, I haven't.
**Acannon**: Okay, so that one's not pushed, but these guys are.
**Acannon**: So three of these guys are pushed to erp.
**Fnjie**: Yeah, but they're all, they're all in the same company.
**Fnjie**: As long as they're all in the.
**Jmendez**: Same company, they're not going to create separate vendor records in Acumatica.
**Jmendez**: They're all related to the same company here.
**Acannon**: So cnc.
**Fnjie**: Yeah, but if you push another one.
**Fnjie**: Yeah, if you, if you push them separately, like if you push all the.
**Jmendez**: Contacts separately and then you give them different codes, I, I would recommend just pushing one of them at.
**Fnjie**: And then.
**Jmendez**: Because if you just push one of them, it's going to Push the whole company.
**Fnjie**: I'll.
**Fnjie**: I'll look at that and see if.
**Jmendez**: We can maybe make it a little bit more error prone proof or error proof where if you can't push the same company to two types, two at the same time.
**Evan.schulte**: Company.
**Fnjie**: Okay, so, but, but I just wanted.
**Jmendez**: To mention here you.
**Fnjie**: So when you, when you push Merit.
**Jmendez**: Contracting for example, you.
**Fnjie**: I would recommend if, if you're going to do that like, like we're saying.
**Jmendez**: Here, maybe you know, contact accounting first but you can also try to search for it.
**Jmendez**: So don't, don't link it yet but.
**Fnjie**: Or don't push it but instead click.
**Jmendez**: Link to ERP vendor and this is going to bring up all of your ERP vendors.
**Jmendez**: So if you just search for Merit here and you.
**Jmendez**: So you could just check Merit and submit that and then you link them.
**Jmendez**: And so now Merit is.
**Jmendez**: Merit's linked.
**Fnjie**: So that I'm guessing that's probably going.
**Jmendez**: To be the case for a lot of the people that you end up trying to push over.
**Jmendez**: They're just, they already exist and they need to be linked.
**Jmendez**: And I would even mention too if you go scroll up here and you go to the Vendors tab, like you're already on the Vendors tab.
**Jmendez**: Go to the Ready to Import tab and then click show suggested matches.
**Jmendez**: Okay, so you don't have any suggested matches.
**Jmendez**: That's, that's interesting.
**Fnjie**: I'll.
**Jmendez**: I'll double check that and make sure that they're just not missing by like one letter or something.
**Fnjie**: But yeah, basically the, the suggested matches feature is really.
**Fnjie**: It's.
**Jmendez**: It's supposed to match up a company in your address book to a company and the acumatica sites.
**Fnjie**: It is possible that you just have.
**Jmendez**: Everybody linked up already too but I'm not sure.
**Jmendez**: I have to double check.
**Acannon**: So is it reading this because there's no drop down menu or any company that, that I can select.
**Acannon**: You type it in manually each time for the company name.
**Acannon**: So is it sorting it by that or is it once you get into, you know, the ERP and you tag it just the way you showed me on that vendor, that's when, that's when it'll link to.
**Acannon**: All of, all of them will be linked to Merit.
**Acannon**: Not by.
**Acannon**: Yeah, not by me typing this in on each company name.
**Fnjie**: Right, Correct.
**Fnjie**: So if you look at like that number up there.
**Fnjie**: So it looks like Merit was actually.
**Jmendez**: It was, it was pushed with that one of those numbers to 243009.
**Acannon**: Yeah, that's the commitment.
**Fnjie**: Yeah but that's the ID that, that.
**Jmendez**: Is the ID of the vendor.
**Jmendez**: You're looking at the vendor right now.
**Jmendez**: So you just linked Merit Contracting and Merit Contracting apparently has, and that's the vendor that you must have pushed with that number, the 24030009.
**Fnjie**: So, but that process, that, that process.
**Jmendez**: That you just did, where you, you pushed Merit, you went to the, you went to the ERP admin tool, you clicked Link, you search for Merit, and then you, you selected them.
**Fnjie**: That is like, that is the best possible process, right?
**Jmendez**: Because you're not creating anything in Acumatica.
**Jmendez**: It already exists.
**Jmendez**: You're just linking it to the other side.
**Fnjie**: It sounds like if you do that.
**Jmendez**: And you don't find one, that accounting might want you to reach out to them before pushing it, just to make sure you're, you know, pushing the way that they wanted to.
**Jmendez**: Or if, you know, maybe you're not searching for the right person or something before you end up pushing it.
**Fnjie**: So do that process that we just did.
**Jmendez**: If, let's say you're creating a commitment, right, it's for a vendor that isn't synced yet.
**Jmendez**: So that button is going to be grayed out.
**Jmendez**: It's not going to let you click push and it's going to say you have to push the vendor first.
**Jmendez**: So do exactly what you just did.
**Jmendez**: You'll go to the vendor, you'll click push on them, you'll go to the ERP admin tool and you'll just click link to erp.
**Evan.schulte**: Right?
**Mcalcetero**: And then if you got to go.
**Acannon**: In here and approve the commitment in here too.
**Fnjie**: Yeah.
**Fnjie**: And the vendor, the vendor side of things, they just, they have to be linked.
**Jmendez**: Once they're linked, you'll never have to link them again.
**Jmendez**: But there is an upfront, you know, work that has to be done, basically.
**Jmendez**: Like if you've never done anything with environmental assurance, in this case in Job Planner, we got either import them or we have to link them.
**Fnjie**: Now, I would say if, you know.
**Jmendez**: Let'S say you're starting a job up right, you know, I'm going to have to work with this person, this person, this person, this person.
**Jmendez**: They're not in my system yet.
**Jmendez**: You can import them from Acumatica.
**Jmendez**: So you don't have to push them or anything.
**Jmendez**: It's just going to bring them in.
**Jmendez**: They're already in Acumatica.
**Jmendez**: So if you go to vendors and your commitment is pushed now so that, you know that that will now show up in Acumatica.
**Fnjie**: So let's say, you know, you're starting.
**Jmendez**: A project, you know you're going to have to work with A, B and C.
**Jmendez**: Right.
**Jmendez**: If you go into vendors or you know, you went into your address book, you tried to add them to your project and you couldn't find them.
**Jmendez**: So they're not in your job planner system yet.
**Jmendez**: So you want to either add them manually or import them.
**Jmendez**: So the first thing I would do is I would go to your ERP admin vendors and then just search right here.
**Jmendez**: So search for, you know, whoever you're looking for and if you find them here, all you have to do is click Import.
**Fnjie**: It's going to create that, that company.
**Jmendez**: In your address book.
**Jmendez**: So like CNC for example here, don't import them because you've got them, you've already got them created.
**Jmendez**: So we're going to want to link them now because you've already created them a job planner but, and the, and the front end if you know, like hey, I'm going to be working with this guy on this project, I know he's an acumatic or he might be and he's not in job planner yet, rather than creating him in Job planner from scratch, come in here, search vendors, find them, import them.
**Fnjie**: And you just, you know, you saved.
**Jmendez**: A ton of time, right, because you just imported all of his information.
**Njepson**: If we haven't worked with someone before, that's why we ask for a company's W9 to issue them a contract.
**Njepson**: So anytime we get a new W9 from someone that we haven't worked for, you send that to accounting and say please enter them as a vendor and they will pop up in here and then you can then write a contract to them because we shouldn't be doing work with anyone that we don't have COI and a W9 from.
**Acannon**: Yes, I do send them.
**Acannon**: Okay, thank you.
**Fnjie**: Yeah, so cool.
**Fnjie**: So in that case then it's probably.
**Jmendez**: Just a best practice just to always import because if you're importing, you know that accounting has looked at it, it's been entered in acumatica and all the work has basically been done for you.
**Jmendez**: They've entered in all that information.
**Jmendez**: So you're just, you're not deduping, you're not re entering in the same information again with that said, there's going to be some like CNC for example, you've got in ready to export.
**Jmendez**: So if you go to ready to export right now, I'm, I believe you have CNC in there.
**Jmendez**: So if you click.
**Fnjie**: Yeah, so what we're going to do.
**Jmendez**: Here is we're going to click on CNC there.
**Fnjie**: Yep.
**Jmendez**: Just link them.
**Acannon**: Understood.
**Acannon**: Yeah.
**Acannon**: The last thing was the issue of who, who can invoice when you assign it here, the invoice contact.
**Acannon**: So we're having issues with them being able to.
**Acannon**: The sub being able to come, come in here.
**Acannon**: If it's not this person, like for instance, deem or electrical contractor.
**Acannon**: The person who invoices has to log into someone else's account to come in here to be able to access the change order and invoices tab up here.
**Acannon**: So they can invoice against our schedule values that we have in the project.
**Acannon**: And then cnc, for example, cannot, can't, can't get access to it at all.
**Acannon**: And I don't know how to help them and guide them.
**Fnjie**: So does it work?
**Acannon**: Sometimes.
**Acannon**: Doesn't work other times.
**Fnjie**: So for those types of things, you.
**Jmendez**: Can direct them to our customer service.
**Acannon**: Yeah, Kristen was helping work on it.
**Fnjie**: But okay, so yeah, one of their.
**Gducharme**: Contacts wasn't connected to the account.
**Gducharme**: But Glenn and I were talking a little bit about the invoice contact because it doesn't seem like just anyone in the company can just look at that commitment.
**Gducharme**: If they're on the company, their specific name has to be attached to it.
**Gducharme**: And they usually, according to Glenn, the, the invoice account or the invoice contact, I'm sorry, changes like per job almost or per project, depending on where it is.
**Gducharme**: And they don't know who it is until after the commitment's already executed.
**Gducharme**: And then by that point they can't update the contact.
**Acannon**: Well, not necessarily.
**Acannon**: I just didn't know that that was how, that's how Job Planner worked as far as the invoice.
**Acannon**: So the project manager who I did the contract with, then they're like, yeah, you know, then I find out later.
**Acannon**: So now that 15 contracts are written or whatever, you know, going forward, I have to set the right person.
**Acannon**: So I know to ask that question up, up front.
**Acannon**: But still that leaves one person to be able to invoice and what if they get fired or you know, leave the company and you know, there's, there's.
**Fnjie**: Technically two because you can either the.
**Jmendez**: The, the person on the subcontract or the invoice contact can do it.
**Jmendez**: I want to mention though, we are working on a change for that.
**Jmendez**: I don't have an exact date on it, but it's currently in process.
**Jmendez**: So basically the company, anybody in the company that's on the subcontract will be able to do all of the Things as long as they're on the project.
**Jmendez**: So if they're on the company, they have access to the project.
**Jmendez**: So like in CNC's example, if you just have one CNC person on there, but four CNC users are on the project, as long as those four CNC users have the proper permissions, there's a permission, you know, permissions underlying them, they will be able to access that subcontract.
**Jmendez**: Now that I know that you guys are probably looking for that, I'll make sure that, you know, as soon as we make that available.
**Jmendez**: In the meantime, though, it sounds like you've got maybe some subcontracts that you have already done.
**Jmendez**: You know, you've pushed them, you approved them, but you've got invoice contacts on those that are different than what you actually want.
**Jmendez**: So you want to change them basically.
**Jmendez**: So we'll make a change to allow you to change that.
**Jmendez**: So you can, in the meantime, you can at least update that invoice contact.
**Jmendez**: So if, you know, somebody contacts you and says, hey, this person isn't the person, I need this person to be able to see it, you can go in there and just change the invoice contact to that person even after it's been pushed and approved and all that stuff.
**Acannon**: Okay, so Kristen, to the one earlier, the guy John was out on vacation or whatever.
**Acannon**: So even if he connects to the account, still nobody else would be able to go in an invoice.
**Acannon**: It still has to come from his account if he's listed as the invoice contact.
**Gducharme**: To my knowledge, currently, just for the moment, yes, until Evan can do that.
**Acannon**: Not even if all, not even if they're all linked to the same company.
**Acannon**: Just the way we just did.
**Acannon**: Did it in the RPN where you're linking people to the company.
**Fnjie**: Yeah.
**Fnjie**: So that's, that's the change that I.
**Jmendez**: Was referring to that, that we're working on.
**Jmendez**: But we don't, it's.
**Evan.schulte**: We're.
**Jmendez**: We're working on it, so we don't.
**Njepson**: That's the same, that's the same thing we, you have to do in Procore.
**Njepson**: Because I think sometimes, you know, let's say you're adding a project manager and it's just going to be up to whatever the subcontractor is.
**Njepson**: But sometimes, you know, project managers don't want for a particular company, like they don't want their other super field guy to be able to view the contract and they would rather him just be able to see the schedule or something.
**Njepson**: So I don't know how you combat that.
**Fnjie**: Well, we, the way permissions.
**Acannon**: Yeah.
**Fnjie**: So, so we're gonna, we're gonna allow.
**Jmendez**: Anybody in the company to view the subcontract.
**Jmendez**: This is a change that we're working on, but it will, it will still rely on the permission.
**Jmendez**: So if you know you have three different users from the same company, but only one of them has permissions to view invoices.
**Acannon**: Okay.
**Jmendez**: Then only that person would be able to invoice.
**Jmendez**: So yeah, you just, the super whoever you'd be able to just restrict from that feature.
**Acannon**: So this is what I was doing, Evan.
**Acannon**: I was given, you know, obviously the project manager, whoever the contact of the invoice invoice contact was.
**Acannon**: I, I'd go in here, give them permissions and then I'd add, you know, another person to the company and go in there and give them the same permissions not knowing whether or not just by naming, just by naming them in the con in the, their company here would tie them to, to that company or not.
**Fnjie**: So yeah, no, I totally, I totally.
**Jmendez**: Understand where you're coming.
**Acannon**: I don't think they can even access to use the permissions.
**Acannon**: Right?
**Fnjie**: Well, yeah, so it, it really comes down currently to who the invoice contact.
**Jmendez**: Or contracted company contact is on that and on that, on that subcontract.
**Fnjie**: So if you go to that merits.
**Jmendez**: Contracting subcontract, you just need to make sure that the person who needs to access or create the invoice is set as the invoice contact for right now.
**Jmendez**: So I know you can't do that on all of your subcontracts right now.
**Jmendez**: For example, the one for environmental assurance, you know, that's been approved and pushed.
**Jmendez**: So it's not going to let you change that.
**Jmendez**: So one thing we're going to do just in the meantime is we're going to, we're going to make a change.
**Fnjie**: To let you modify that so you'll.
**Jmendez**: Be able to change all the invoice content down.
**Jmendez**: Okay, cool.
**Jmendez**: And then down the line, I, I probably in a couple weeks we'll have, we'll be having the change come out where at the company level.
**Jmendez**: It'll work like you're saying, so it'll let any company, it's something that we're already working on.
**Jmendez**: So just coincidentally, you guys are looking forward as well.
**Jmendez**: So we'll make sure to let you know when that's available.
**Jmendez**: But yeah, in the meantime, just go into those and set the invoice context.
**Jmendez**: If you have somebody else that needs to access It.
**Evan.schulte**: Right.
**Acannon**: That helps a lot.
**Acannon**: Thank you.
**Evan.schulte**: Cool.
**Fnjie**: Yeah, anytime.
**Fnjie**: I'm more than happy to do a call anytime, man.
**Jmendez**: So if you have any questions, I think calls tend to be quite a bit more productive.
**Jmendez**: It's, there's just a lot of stuff to go over.
**Jmendez**: It's hard to do it over email sometimes.
**Acannon**: It's just the last couple of little questions that fill in, fill in the rest of the rest of the blanks.
**Acannon**: So.
**Fnjie**: Yeah, yeah, yeah.
**Jmendez**: And I'm sure, I'm sure little things will come up here and there in the meantime and just feel free to reach out.
**Jmendez**: We're more than happy to help.
**Jmendez**: And jump on a call.
**Ataylor**: I do have one more question about the vendors.
**Ataylor**: So I know I went in and I searched for the subcontract code that Glenn had on his job.
**Ataylor**: They all created duplicate vendors in, on the, the acumatica side.
**Ataylor**: So how do we fix that?
**Fnjie**: Yeah, so that's, that is, I think we just resolved that from happening in.
**Jmendez**: The future because we talked about that link option, but because they were being just pushed without checking before, I, I, I'm not surprised.
**Jmendez**: So what we can do is we can unlink those vendors and then just relink them.
**Fnjie**: Do you know, I can check, I.
**Jmendez**: Can probably check on my end and.
**Fnjie**: Do like a, I probably have to do it after, after the call, but.
**Jmendez**: I could find out which ones might be affected.
**Jmendez**: But if you know which ones are.
**Fnjie**: Duplicated, that would help too.
**Ataylor**: Yeah, I can, I have the ones that we push towards with the subcontract number from Job Planner.
**Ataylor**: So I'll send you an email with a list of what they are now and what they need.
**Ataylor**: What they need to be linked to.
**Evan.schulte**: Okay.
**Fnjie**: Yeah, that'd be great.
**Fnjie**: And just to show you too.
**Fnjie**: And we'll go ahead and do this.
**Jmendez**: Kind of hopefully save you guys some time.
**Jmendez**: I want to show you really quick in case this does happen in the future.
**Jmendez**: Let's say Merit was linked to the, to the wrong person, right?
**Jmendez**: So you can, in the address book here, you can search for Merit and it doesn't matter which contact you click.
**Jmendez**: I can click Abby or Keegan.
**Jmendez**: It's going to show me the company.
**Ataylor**: And then you're not sharing your screen anymore.
**Jmendez**: Oh, oh, I'm sorry, I'm sorry, I forgot somebody else started sharing.
**Jmendez**: I took it over.
**Jmendez**: So here in the context section, if you just search for Merit here, I'll click Abby here.
**Jmendez**: And I can see that Abby's linked to 2403009.
**Jmendez**: So this is probably one of Them that's a duplicate.
**Jmendez**: So what we can do is we can unlink from ERP and then this is going to.
**Jmendez**: And I'll do this when I get that list.
**Jmendez**: I won't do this right now, but you click on link, it's gonna basically remove this link and then you can just start the process from scratch.
**Jmendez**: So this, this is no longer linked.
**Jmendez**: So we can go into ERP admin.
**Jmendez**: We can go over here to the.
**Jmendez**: Yeah, we got like a background noise or something from somebody.
**Evan.schulte**: Got some music.
**Mcalcetero**: Are you listening to aj?
**Mcalcetero**: That was horrible.
**Bclymer**: That was.
**Bclymer**: I recorded aj.
**Fnjie**: Come on.
**Fnjie**: Everybody's got their music taste.
**Fnjie**: So.
**Fnjie**: Yeah, anyway, so you.
**Jmendez**: Once you unlink them, you can just come back in.
**Fnjie**: You basically you can re.
**Jmendez**: Push it.
**Jmendez**: So you re push it and you can come in here.
**Jmendez**: And I want to mention too, there's actually two ways to link.
**Jmendez**: So if you push the vendor.
**Jmendez**: So like in this case, goodwill of central and Southern Indiana is ready to be pushed.
**Jmendez**: I can link to ERP and I can do the search all in here.
**Jmendez**: Right.
**Jmendez**: I can also go to ready to import and I can do it this way too.
**Jmendez**: So like, if I found merit in here, I could link that to an existing contact within the address book.
**Jmendez**: So it kind of.
**Jmendez**: It kind of lets you do it two different ways.
**Jmendez**: But anyway, so just to.
**Jmendez**: Just to reiterate, you would find the contact, you would unlink and then you would just push it again and basically do the linking process.
**Jmendez**: We'll do that for the list that you send us.
**Jmendez**: I just wanted to mention that, you know, in case you have one that happens in the future, you know how to.
**Jmendez**: How to fix it.
**Ataylor**: Okay, thank you.
**Jmendez**: Yeah, absolutely.
**Fnjie**: Alrighty.
**Fnjie**: Any other questions, comments, concerns?
**Mcalcetero**: One last thing.
**Mcalcetero**: We have accounting on here too.
**Mcalcetero**: Like when we write a purchase order to a material supplier, then they try to send us invoices.
**Mcalcetero**: And this is like Core and Maine specifically.
**Mcalcetero**: And I'm asking accounting as first, when you get invoices from.
**Mcalcetero**: For a job, for a sub that has a purchase order, like between us, we got it.
**Mcalcetero**: Like either we tell you to kick it back, they need to build through job planner, or if, you know, if some of those things have already come through or you guys are able to sort that out on that end so it doesn't show up as an added cost to their po because if it is added materials, then it needs to be a change order written to that purchase order.
**Jdawson**: Is that the sync issue for the purchase order, Jesse?
**Jmendez**: I'm sorry, is it.
**Jdawson**: Is that the sync issue?
**Jdawson**: Because for the foreign main, I believe Brandon has already created.
**Ataylor**: Let's go that one.
**Jdawson**: Some of the PO invoices, it's under po.
**Jdawson**: It was already successfully synced to Akumatica.
**Ataylor**: So I think what Jesse is asking is if accountant receives an invoice and there's already a P.O.
**Ataylor**: we need to kind of coordinate and let them know, hey, we received this invoice, there's a PO they need to build through Acumatica.
**Ataylor**: Is that right, Jesse?
**Mcalcetero**: Right.
**Mcalcetero**: Because otherwise it's going to show up that we still own.
**Mcalcetero**: You know, if it gets paid and not billed through Job Planner, then it'll act like they haven't billed for their purchase order and owe that money.
**Mcalcetero**: Plus it'll show cost to date of all these invoices that are not applied to the purchase order.
**Mcalcetero**: So it's really for everything.
**Mcalcetero**: If you're a project manager and you see something in notion, that's a.
**Mcalcetero**: A bill, but it's from a purchase.
**Mcalcetero**: A company we wrote a PO to, we need to send it back.
**Mcalcetero**: And then, you know, whoever got that invoice needs to notify them or the PM needs to notify that company.
**Mcalcetero**: They need to get in Job Planner and do that billing.
**Njepson**: So do.
**Njepson**: Because Procore and POS did not like talking with Acumatica.
**Njepson**: With Job Planner.
**Njepson**: Can you link a PO invoice with Acumatica?
**Ataylor**: Yes.
**Jdawson**: Yes.
**Acannon**: That's nice.
**Evan.schulte**: Yeah.
**Ataylor**: The only thing that is coming from Acumatica into Job Planner is the direct cost items.
**Ataylor**: That should be it.
**Ataylor**: Everything else should be becoming the other way around.
**Njepson**: Nice.
**Fnjie**: Yes.
**Fnjie**: Yeah.
**Fnjie**: And they do come the other way.
**Fnjie**: Like if you were doing what was.
**Jmendez**: Explained where you did create that invoice on the Acumatica side, we do pull those in, but there are exceptions to that.
**Jmendez**: For example.
**Jmendez**: Well, actually, in this exact case, that would be an exception.
**Jmendez**: So if you create an invoice on a PO in Acumatica and that PO originated from Job Planner, we won't pull that in as a direct cost because what ends up happening is it duplicates your cost.
**Jmendez**: So you already have that cost on the project, on the commitment.
**Jmendez**: So pulling that direct cost in is just going to duplicate whatever was on that direct cost.
**Jmendez**: So we won't pull it in, but the issue would still remain where that PO is showing as unbilled, basically.
**Jmendez**: So the most ideal scenario is you create that invoice for the PO in Job Planner and you push that to Acumatica and then you can fully track all of your billing then.
**Evan.schulte**: Right.
**Jmendez**: In Job Planner you can go to any of your commitments and you can tell exactly how much has been billed and how much is remaining on them.
**Jmendez**: And with that said too, actually we just, we just came out with a new feature.
**Jmendez**: So you'll, you'll see that when you go to release retainage.
**Jmendez**: So we now will, we now do the retainage release as well.
**Jmendez**: So if you, when you do billing for this is more on the receivable side probably for you guys.
**Jmendez**: But when you do retainage billing.
**Jmendez**: Well, actually no, you probably do keep retainage for your commitments as well.
**Jmendez**: So when you do those retainage billings, your final billing will allow you to release retainage on that commitment as well.
**Jmendez**: So you can basically do the all the progress billings and then when you're finally ready, you can release retainage draw within jobliner.
**Njepson**: So meaning they don't have to do two separate invoices because in the past they would have to invoice for the job complete and then they would have to do a separate retainage invoice.
**Fnjie**: You do have to do it.
**Jmendez**: It does create a separate retainage invoice in Acumatica and in Job Planner, but it doesn't make you do a manual process of creating the invoice.
**Fnjie**: I don't have it.
**Fnjie**: I, I don't know if you guys.
**Jmendez**: Have any projects that have retainage invoices right now.
**Jmendez**: I could show you if you did.
**Jmendez**: But basically when you go to the, to the contract, if you have retainage kept in acumatica for that contract, you'll have a button right on the contract right up here next to unlink.
**Jmendez**: It's like to the right of it and it'll say release retainage.
**Jmendez**: And if you click that button, it's, it's just going to basically push to erp.
**Jmendez**: It'll be waiting in your ERP admin to be, to be released and approved.
**Jmendez**: Once you approve that, it's going to automatically create that, that retainers release invoice in acumatica and it'll also create an invoice in Job Planner to reflect that retainers release basically.
**Fnjie**: But it's not effectively, you just don't.
**Jmendez**: Have to create the manual invoice, it'll just create it for you.
**Ataylor**: Can you release like partial retainage?
**Fnjie**: Currently we, we cannot release partial retainage.
**Fnjie**: So it's, it's something that we, we will do.
**Jmendez**: You know, it's, it's something that as soon as somebody says, hey, this is something we need, you know we're going to do it.
**Ataylor**: Yeah, I think we've, we've had quite a Few jobs where we released, you know, partial retain age.
**Jmendez**: On the payable side.
**Ataylor**: Yes, on the payable side.
**Jmendez**: Okay, that's good to know.
**Jmendez**: I will go ahead.
**Jmendez**: I like to be kind of, in.
**Fnjie**: Fact, I, we added that retainage release.
**Jmendez**: To be ahead of the curve for knowing that somebody was going to want that.
**Jmendez**: So I will try to be ahead of it on that one too and add away to partial release retainage.
**Jmendez**: If we were to add that would.
**Fnjie**: Do you guys have a common.
**Jmendez**: Where you, you do a partial release at a line item level?
**Jmendez**: Like you say, this line, I want to release 50, this line I want to release 100.
**Jmendez**: Or is it more just across the board?
**Jmendez**: I want to release 50% or 75%.
**Ataylor**: I mean, I, I would think the line item would be better.
**Evan.schulte**: Okay.
**Ataylor**: If anybody else wants to chime in on that.
**Njepson**: I, I've never had to release partial retainers, so I, I don't know.
**Fnjie**: Okay, yeah, no problem.
**Fnjie**: I think, I think that makes sense.
**Jmendez**: Anyway, to do it at the line item level.
**Jmendez**: That's the most granular.
**Jmendez**: And if you think that's going to be a case that you need, then it makes the most sense to go that granular.
**Jmendez**: Because when we do go that granular, you always have the, you still have the high level control.
**Jmendez**: Even if you didn't want to do 75, 50, 20, you could just do 75 on all the lines.
**Jmendez**: So we will, we will get that done.
**Jmendez**: Alrighty, cool.
**Fnjie**: Anything else?
**Gducharme**: Oh, just raised his hand.
**Jmendez**: Yes, sir.
**Acannon**: Yes, sir.
**Acannon**: Back real quick with when.
**Acannon**: Show my screen when, when these expenses go in, they hit.
**Acannon**: And this is all, this is all that's in there.
**Acannon**: There's no copy, there's no receipt, no description.
**Acannon**: And this is, how is this, how does this look when you guys put it in acumatica or, or whatever it is to, to, to get put in here so we can, we can see this.
**Acannon**: Because I don't see these invoices or receipts.
**Acannon**: They just go, they go to you guys.
**Acannon**: And I got, I got sent it to code.
**Fnjie**: Go to the, Go to the direct costs.
**Fnjie**: Click on one.
**Fnjie**: Go to schedule of values.
**Fnjie**: So there's also this here.
**Jmendez**: Did you, did you see this as well?
**Acannon**: Yeah.
**Acannon**: What is it?
**Acannon**: What is.
**Fnjie**: So we're, we're pulling in.
**Jmendez**: Well, we're, we're pulling in everything on the transaction.
**Jmendez**: I think it's possible.
**Fnjie**: Maybe if you can point out something.
**Jmendez**: That we're not, I'd be happy to pull.
**Njepson**: Did you notice, Glenn, is your question.
**Njepson**: You didn't code this one, so you're one.
**Acannon**: I coded it.
**Acannon**: I know what it is.
**Acannon**: But when there's 150 of these, I'm not going to remember what every one of them is.
**Acannon**: I.
**Acannon**: I do know what this, what these two are.
**Acannon**: I know what all.
**Acannon**: I know what these three are.
**Acannon**: I do not know what this is.
**Acannon**: This was the.
**Acannon**: This.
**Acannon**: This was for.
**Acannon**: All of this is for groundbreaking.
**Acannon**: So.
**Acannon**: But there's several.
**Acannon**: Several transactions that we coded to groundbreaking that.
**Acannon**: That are still not here.
**Acannon**: I mean, there's a dozen transactions that are still not showing up here.
**Njepson**: They will eventually, but I guess I don't know what the answer is.
**Njepson**: Are you asking there to be.
**Njepson**: When it pushes over to be.
**Njepson**: You want like a picture of the receipt or what are you after?
**Acannon**: I mean, a description or.
**Acannon**: Yeah, what it is or.
**Acannon**: Or an attachment.
**Mcalcetero**: If.
**Acannon**: If I don't know if they can scan in the.
**Acannon**: Scan the receipt or just not scan it.
**Acannon**: But yeah, attach it.
**Acannon**: Because it usually comes in an email.
**Acannon**: Like I.
**Acannon**: When I have a receipt, I just scan it and attach it.
**Acannon**: But yeah, when they get invoices.
**Acannon**: But they may.
**Acannon**: They may put it in acumatic and it just isn't coming over.
**Acannon**: That's what I'm asking.
**Acannon**: I don't know.
**Fnjie**: Yeah, we do not pull in any.
**Jmendez**: Attachments currently with it.
**Jmendez**: So if it is in there, we're not pulling in.
**Fnjie**: But good.
**Jmendez**: We're pulling in the description of the cost.
**Fnjie**: So would it be possible to just.
**Jmendez**: Put a description that would maybe kind of say what it is?
**Fnjie**: Because currently this description for this, this.
**Jmendez**: Cost in acumatic is VSP Star Personal Concepts.
**Jmendez**: And if this was like a description that maybe said a little bit more.
**Acannon**: Yeah, I have no idea what this is.
**Njepson**: So I'm assuming Personal Concepts is the vendor.
**Acannon**: I don't know.
**Njepson**: Jesse, what do you think?
**Njepson**: Do you think this is enough or.
**Jmendez**: On what.
**Evan.schulte**: I'm sorry.
**Jmendez**: This is a expense that's being pulled in on a job for VSP Personal Concepts.
**Jmendez**: Glenn's saying he doesn't know.
**Fnjie**: He said his main concern is if.
**Jmendez**: There'S a bunch of these, he doesn't think there's enough information on it to know what it is.
**Mcalcetero**: Do you know who VSP is?
**Jdawson**: I.
**Jdawson**: I think this is from credit card.
**Jdawson**: This is what we got in the statement.
**Jdawson**: So this is usually our basis for the description.
**Evan.schulte**: Okay.
**Acannon**: And it.
**Mcalcetero**: It went in and there's no copy of the.
**Acannon**: No attachment?
**Njepson**: No, that would all be on notion.
**Njepson**: It's probably a lot of work to have to attach a receipt to each one.
**Ataylor**: Attachment.
**Ataylor**: Yeah, attachment will be in notion.
**Mcalcetero**: Well, no.
**Mcalcetero**: So this.
**Mcalcetero**: You're seeing this from notion or where are you seeing this?
**Acannon**: This is in job planner, Jesse.
**Acannon**: This is.
**Acannon**: Here, I'll show you.
**Acannon**: Just so my.
**Acannon**: My question kind of is like, I have, you know, still no, no, no credit card transactions for two months have been posted to this budget, even though they're encoded back.
**Mcalcetero**: Back to that expense.
**Acannon**: And yes.
**Mcalcetero**: Click on it.
**Mcalcetero**: There's no way for that.
**Mcalcetero**: Like in procore, you click on it, it would.
**Mcalcetero**: I believe you could.
**Mcalcetero**: I don't know if you could see the invoice.
**Mcalcetero**: I think it would have a link that would take you to the invoice or the receipt.
**Mcalcetero**: So we don't have that ability.
**Evan.schulte**: You couldn't.
**Njepson**: You could not view the receipt in procore?
**Njepson**: No, but I mean, if.
**Njepson**: If you're diving into it, you.
**Evan.schulte**: You.
**Mcalcetero**: I don't know, does it let you code it?
**Njepson**: So you should know what it's for and be able to know.
**Njepson**: And then if you have to see the receipts stored somewhere.
**Mcalcetero**: Well, not unless you're the one that, you know, some receipts, like my receipts, go to all different types of jobs.
**Mcalcetero**: So does it tell you.
**Mcalcetero**: Do you have the option of saying who coded and approved the transaction?
**Mcalcetero**: Can that info be put into.
**Evan.schulte**: Either.
**Mcalcetero**: Acumen and it pulls over into job planner.
**Fnjie**: So.
**Fnjie**: So you're looking for who co.
**Fnjie**: Like.
**Jmendez**: Who created the transaction, at least then.
**Mcalcetero**: If the PM doesn't know what it is, he can contact that person.
**Jmendez**: I can check to see if we can import that.
**Jmendez**: I know.
**Evan.schulte**: Check to see if we can pull.
**Jmendez**: In who created transaction on direct cost.
**Fnjie**: Yeah, we.
**Evan.schulte**: I'll.
**Jmendez**: I'll look to see if we can pull that in.
**Jmendez**: I think ultimately it's just a matter of making sure that there's enough information on that.
**Fnjie**: And if.
**Jmendez**: If that's a matter of us pulling in for something that's already there, that we can give you more information, then that's cool.
**Jmendez**: Or if it's a matter of changing the description or something.
**Fnjie**: But if it's like, if this is.
**Jmendez**: Some automated import that's occurring due to a credit card transaction, then obviously I understand you wouldn't.
**Jmendez**: You wouldn't be able to modify every single one of those too.
**Acannon**: So.
**Fnjie**: So, see, basically what we're pulling in.
**Jmendez**: Is we're pulling in the.
**Fnjie**: There's really two different things.
**Jmendez**: There's expenses and then there's bills.
**Jmendez**: There's project transactions which include bills, but then we're pulling in bills separately.
**Jmendez**: And when we pull those in, they have a description on them and then on the item itself, and then Every line has the option to have a description on it, and we're pulling in both of those in.
**Jmendez**: So, like, in that case there, the item only had one description, which was the bsp.
**Fnjie**: I'll.
**Fnjie**: I'll.
**Jmendez**: I'll just kind of do some spot checking on our end on those individual transactions just to see if there's anything in the data that we're getting that we can kind of throw in to somewhere else on the direct cost too, just to include as much information as possible, kind of, you know, if.
**Jmendez**: Even if it's a little bit too much, you know, we'll just include as much as possible because it reads off.
**Acannon**: Of whatever they put in Acumatic.
**Acannon**: Correct, Evan?
**Jmendez**: Correct.
**Fnjie**: Yep.
**Acannon**: Yeah, so whatever.
**Njepson**: Whatever.
**Acannon**: The script, whichever box that they're putting a description, it seems like it's just an automated thing.
**Acannon**: So if we can figure out how to edit that one box, it would be.
**Acannon**: At least say what it is.
**Acannon**: But like AJ said, you know, the.
**Acannon**: We'll have the copy of it somewhere in an email or.
**Acannon**: Or in Notion.
**Acannon**: But I mean, that information gives us just nothing at all.
**Ataylor**: Oh, that information is in Notion.
**Ataylor**: So if you go in Notion and then you click all and just search.
**Ataylor**: If you click all and search for VSP or search for that amount, you would see it and the receipt is attached in there as well.
**Njepson**: I know we're definitely.
**Njepson**: We're still working through the kinks on Notion too, Glenn.
**Acannon**: So, yeah, yeah, I don't.
**Acannon**: I haven't gotten a whole lot of invoices or.
**Acannon**: Or stuff linked to me on Notion compared to the amount of transactions that have happened.
**Acannon**: So I can count seven things that have sent to me on Notion and there's been dozens of transactions that should have been sent to me for coding.
**Acannon**: So I'm just.
**Acannon**: I'm waiting.
**Acannon**: I keep asking.
**Acannon**: I don't know each week kind of where they're at and if.
**Acannon**: If they're coming, just trying to keep up on them, you know, we.
**Ataylor**: We have to wait until the statement ends.
**Ataylor**: The statement and ended just yesterday.
**Ataylor**: So we will be working on uploading it once the statement ends.
**Ataylor**: So the statement ending date is the 22nd.
**Acannon**: What about for stuff that's already been coded?
**Acannon**: When does it take another month to hit the budget at that point or if.
**Ataylor**: If.
**Ataylor**: No, it doesn't.
**Ataylor**: Like I said, with the issues we've been experiencing with the upload, we just want to make sure that it's right before we upload it again and then have the same issues hidden.
**Ataylor**: The project.
**Ataylor**: Incorrect project task.
**Ataylor**: So we are Working with Acumatica to get that upload figured out.
**Fnjie**: Yeah.
**Jmendez**: And like I said, too, if there's anything that we can do to help with that, please let me know.
**Fnjie**: We're not as experienced as Acumatica themselves.
**Jmendez**: With Acumatica, but, you know, we're.
**Jmendez**: We have some good experience and if, you know, if there's any modifications that we can make on our end, we're more than happy to.
**Jmendez**: To work with you guys to do that.
**Acannon**: Yeah, I'm just.
**Acannon**: I'm the new guy, so I've learned it all.
**Acannon**: The.
**Acannon**: All the ways everything tries to connect without seeing.
**Acannon**: It's not.
**Acannon**: I can't see.
**Njepson**: Don't feel bad.
**Njepson**: We're all new to this, especially Job Planner and Notion, so.
**Fnjie**: Yeah, man, definitely.
**Fnjie**: And this gets.
**Evan.schulte**: Definitely.
**Njepson**: Appreciate you being the guinea pig, though.
**Evan.schulte**: Yeah.
**Jmendez**: I mean, you're.
**Njepson**: Get all the kinks figured out before my job's starting here, please.
**Fnjie**: Yeah, this is.
**Acannon**: Yeah, Evan spent about an hour with me last week or a week before.
**Acannon**: And Evan is like.
**Acannon**: He's the lead developer.
**Acannon**: He built this platform, so he was able to go ahead and fix my.
**Mcalcetero**: What's the date on that transaction you were referencing earlier?
**Acannon**: Me?
**Mcalcetero**: Yes.
**Acannon**: Which.
**Acannon**: Which transaction?
**Mcalcetero**: The one you couldn't figure out where it was from.
**Jmendez**: It's called VSP Person.
**Jmendez**: It's got the name of it is the description as VSP Star Personal Concepts.
**Mcalcetero**: And the date that shows.
**Fnjie**: Yeah, the date that's showing on it is actually the date that it was.
**Jmendez**: Imported into Job Planner.
**Fnjie**: This is.
**Fnjie**: It's something that we.
**Fnjie**: We haven't.
**Fnjie**: Yeah, we.
**Jmendez**: Sorry, go ahead.
**Evan.schulte**: Oh, I could.
**Fnjie**: I could get the date of it.
**Ataylor**: The.
**Ataylor**: The dating notion is February 26th.
**Ataylor**: Transaction date February 26th, and it was actually on your card, Jesse.
**Acannon**: Okay, I.
**Acannon**: I honestly don't.
**Mcalcetero**: Yeah, that was posters.
**Mcalcetero**: The labor law posters for your job.
**Acannon**: Yeah, but you see.
**Acannon**: I mean, you see my point on why.
**Acannon**: What.
**Acannon**: What this is like.
**Jmendez**: We have.
**Acannon**: We have a team of people trying to figure out what.
**Acannon**: What.
**Acannon**: Where 30 bucks went instead of just having a description.
**Acannon**: So I don't know if maybe the process could be.
**Acannon**: Hey, you know, stuff comes to the PM first, and that way we can code it and put a description in and then send it to accounting to put it in Acumatica or.
**Acannon**: Because when, you know, everybody invoices us for something that goes to accounting first, right?
**Acannon**: Jesse, that's your.
**Acannon**: That's our process.
**Mcalcetero**: These are credit card transactions.
**Acannon**: This one is.
**Acannon**: Yes, but not all of them.
**Acannon**: That the 29 is with those two charges for 342 was the equipment rental and the 107 was also an invoice equipment rental.
**Mcalcetero**: So they, they get an invoice and they send it to you.
**Mcalcetero**: If you're the PM on a job, you're the one that gets it.
**Acannon**: Yes, but I, I can't, I can't make this description is what I'm trying to tell you.
**Acannon**: They do it in acumatica and then it pulls in the job planner.
**Acannon**: So I can code it, but.
**Jmendez**: But you can't specify a description or anything on.
**Acannon**: Right, right.
**Acannon**: So as the project builds and there's, you know, dozens and hundreds of these across the, the project that's.
**Acannon**: It's time consuming to go back and especially it doesn't even give me the actual transaction date and take it would.
**Acannon**: It just eats up time having to go back and backtrack and see what the heck these things are for.
**Acannon**: Did I pay someone twice?
**Acannon**: You know, we already buy this.
**Fnjie**: Yeah.
**Fnjie**: As far as the transaction date goes.
**Jmendez**: That'S something we can definitely address.
**Jmendez**: We can make a change to actually import the real transaction date and override the created on date.
**Jmendez**: Normally the created on date in our system kind of says like this is the date that this thing was created.
**Jmendez**: But because of this special scenario where it's being imported from something that was technically created in the past, we can just override that.
**Fnjie**: So yeah, that, that hurdle is absolutely.
**Jmendez**: Something we can get over now.
**Jmendez**: In terms of the description vsp, I'm just looking at that transaction here.
**Acannon**: So let me see an example of one that was an invoice here.
**Acannon**: So tree removal, westfield, make a path and cover it with wood chip.
**Jmendez**: So I'll give you one example here.
**Fnjie**: So that VSP Personal Concepts one.
**Fnjie**: There's actually a couple transactions for that.
**Fnjie**: Not on this job specifically, but just.
**Jmendez**: Across the whole system.
**Jmendez**: And there's another one here that's coded as CC9088.
**Jmendez**: Alex underscore VSP personal concepts.
**Fnjie**: So it seems like that one has.
**Jmendez**: A little bit more information in it.
**Jmendez**: That one was created on March 7th.
**Fnjie**: So it, if, let's say it said that if, if it's.
**Jmendez**: Instead of it saying VSP Personal Concepts, it said like credit card and then the last four digits and then underscore like the, the person's name underscore VSP Personal Concepts.
**Acannon**: And then Personal Concepts, labor law posters is what would be, is what would be helpful?
**Fnjie**: Well, yeah, yeah, of course.
**Fnjie**: That would be the most ideal.
**Jmendez**: I'm just looking at transactions you guys already have in the system and I, I see that you Already have one with CC9088 Alex in it.
**Jmendez**: So I'm just wondering if that's something.
**Fnjie**: That maybe you, you guys changed how.
**Jmendez**: You'Re entering those in or something because that's a more recent transaction.
**Jmendez**: That one's from the March 7th.
**Acannon**: I have no idea.
**Acannon**: That probably could be when they saved it on their computer.
**Acannon**: That's what it saved as.
**Acannon**: And then they dropped it into their email and sent it out.
**Acannon**: Any, any description that I have, that I have put in any of mine anyways, is, is a description of what it is, not.
**Acannon**: Not a code or something like that.
**Fnjie**: Yeah, I guess what, what I'm.
**Fnjie**: What I'm mainly what I'm saying is.
**Jmendez**: This is another VSP Personal Concepts transaction, but it has more information description.
**Jmendez**: So unlike this one you're showing us where it just has VSP Personal Concepts.
**Jmendez**: This one has more information which implies to me that somewhere there's more information being added to these transactions.
**Jmendez**: I'm just wondering where or when that's occurring.
**Acannon**: And like you said, it's not on Westfield Collective's job, right?
**Ataylor**: I would know those transaction.
**Ataylor**: Those descriptions are what come over from the credit card card.
**Ataylor**: So when these get, and I'm just referring to the vsp, when they get pushed into Notion, when you guys are adding the codes, you have the option to change the description because at that point if you have the receipt, it matters.
**Ataylor**: It makes sense to just go ahead and change the description.
**Ataylor**: So when it, when you have it on your job, you'll know exactly what it is.
**Acannon**: Okay.
**Acannon**: Yeah.
**Acannon**: Okay, if we can do that Notion.
**Ataylor**: Then yeah, you can change it in Notion and on the invoices.
**Ataylor**: I will talk to, to Brandon.
**Ataylor**: I think it'll be helpful if you guys have re read only access to Acumatica.
**Ataylor**: That way you can go in and be able to look at actual invoice copies on your job.
**Ataylor**: So I'll talk to him about that and see if he's okay with that.
**Ataylor**: I can give you guys access to Acumatica.
**Acannon**: Yeah, it helps to see all, all the, all the parts in the, in the chain.
**Fnjie**: And to be honest, ours, our, our.
**Jmendez**: Goal is to make that never a requirement.
**Jmendez**: So if there is information in Acumatica on these transactions that you want to be pulled in that isn't currently being pulled in, please let me know because.
**Fnjie**: We, yeah, we want to pull in.
**Jmendez**: As much information as.
**Jmendez**: As you need to be able to tell like what these transactions are.
**Jmendez**: We're obviously just limited on what's actually in Acumatica.
**Fnjie**: So I honestly it sounds like to me, if you were to reco.
**Jmendez**: When you recode those.
**Jmendez**: If, like in this VSP example, if you were to change the description on that notion when you're, you know, initially sent those transactions, you just changed it to vsp, you know, posters or whatever you want to call it.
**Fnjie**: That'S.
**Jmendez**: Then that'll go in acumatica with that description.
**Jmendez**: It'll come into Job planner with that description.
**Jmendez**: And in that case, you really.
**Jmendez**: It doesn't.
**Jmendez**: I don't think you'd have to go into acumatica.
**Fnjie**: All right, so I got a couple things to follow up with here.
**Fnjie**: One, I'm just, I'm going to double.
**Jmendez**: Check these direct costs.
**Jmendez**: Just make sure there's nothing else that we can pull in.
**Jmendez**: I'm looking at them right now and I don't think there is.
**Jmendez**: Just based on what I'm.
**Jmendez**: What I can see, it's really.
**Jmendez**: That description is like the bulk of it.
**Jmendez**: So if you can get something in place to.
**Jmendez**: If you need to change that description before it goes in acumatica, I would definitely recommend that if you do change it after it goes in acumatica, that's still going to be pulled into.
**Jmendez**: So if you import it and you realize you need more information and you go and change it and the acumatica side, that's totally fine.
**Jmendez**: And I'm going to look into partial retainage.
**Jmendez**: I'm going to add a way to change the invoice contact on your commitments after it's been pushed so you can give access to people, you know, after the fact, basically.
**Jmendez**: And then we're going to also see if we can pull in who created the transaction.
**Jmendez**: If we can pull then that, you know, it might give a little bit more information and help you kind of research it.
**Jmendez**: Ideally though, you know, we get that description and we don't even have to research.
**Jmendez**: You can just look at the transaction and you can tell immediately what it is.
**Mcalcetero**: Yeah, I think that'll help a lot.
**Mcalcetero**: I didn't know we could change the description of it.
**Mcalcetero**: If we can do that makes it easy.
**Evan.schulte**: Okay, cool.
**Fnjie**: Alrighty.
**Fnjie**: Yeah, so I will make sure that.
**Jmendez**: I follow up on these.
**Jmendez**: It'll probably take me a day or two to, to get a full answer on these.
**Jmendez**: But the one where we're gonna make it so you can change the invoice contact, I'll basically reply with our, you know, kind of a summary on all these.
**Jmendez**: But that will be deployed.
**Jmendez**: So as soon as you hear back from me, we'll.
**Jmendez**: We'll have that deployed.
**Jmendez**: By then, and then anything in the meantime, please let us know.
**Jmendez**: Like we were saying for that import, if there's anything we can help with, we're here to help on that.
**Jmendez**: Anything else?
**Jmendez**: Any other questions?
**Evan.schulte**: Okay, great.
**Jmendez**: Well, thanks for staying, guys.
**Jmendez**: This is a long call.
**Jmendez**: I know everybody's probably wanting to go, but I do appreciate everybody's time, and I.
**Jmendez**: I'm glad we got.
**Jmendez**: We're getting this worked out.
**Bclymer**: Thank you, Evan.
**Bclymer**: Thank you, Chris.
**Bclymer**: And anybody guys have questions, don't forget to reach out and don't forget for the recording.
**Bclymer**: Chris and I appreciate it.
**Gducharme**: Of course.
**Bclymer**: Thank you so much.
**Bclymer**: Thank you, guys.
**Gducharme**: Thank you.
**Fnjie**: Thanks, everybody.
**Jmendez**: Have a good day.
**Mcalcetero**: Yeah.
**Evan.schulte**: See you.
**Evan.schulte**: Bye.