# Core Engineering Patterns: Systemic Code Issues

## **Primary Development Anti-Patterns**

• **Utility Function Proliferation**

- Teams create local implementations instead of importing shared utilities
- Same validation logic written 3+ times across modules
- Results in maintenance drift and behavioral inconsistency

• **Configuration Fragmentation**

- Multiple entry points for same configuration data
- Hardcoded values scattered throughout instead of centralized
- No single source of truth for operational parameters

• **Global State Overuse**

- Singleton patterns everywhere to avoid proper dependency injection
- Cache variables in multiple modules creating state management complexity
- Memory accumulation and potential state corruption risks

• **Copy-Paste Development Culture**

- Script templates duplicated without abstraction
- Import patterns copied inconsistently across modules
- Backwards compatibility aliases preserved indefinitely

## **Root Cause Analysis**

**Engineering Culture Issue**: Development teams default to "implement locally" rather than "reuse shared"

**Process Gap**: No enforcement mechanism for shared utility adoption

**Architecture Drift**: Evolutionary development without systematic refactoring discipline

## **Strategic Impact**

**Maintenance Velocity**: Changes require updates across 3-4 locations
**Code Quality**: ~40% redundant utility code across modules
**Operational Risk**: Configuration inconsistency due to fragmented access patterns
**Technical Debt**: Backwards compatibility pollution masking architectural clarity

## **Pattern Recognition**

This is a classic **"Commons Problem"** - shared utilities exist but teams find it easier to implement locally than navigate import dependencies. The codebase shows good architectural intent undermined by tactical development shortcuts.

**Core Fix Strategy**: Enforce shared utility adoption through tooling rather than documentation.

    {
      "Action Request Number:": "2015-00018",
      "Title": "A14 and A15 conveyor containment problems",
      "Initiation Date": "2015-01-05T00:00:00",
      "Action Types": "Reliability Action Request",
      "Categories": "Production",
      "Requested Response Time": "7",
      "Past Due Status": null,
      "Days Past Due": null,
      "Operating Centre": "OC4/5 Calcination and Shipping",
      "Stage": "Action Plan Implemented - Actions Effective - Closed",
      "Init. Dept.": "KW050R",
      "Rec. Dept.": "KW050R",
      "Recurring Problem(s)": "Yes",
      "Recurring Comment": "Containment of spillage and carry back from the A14 and A15 conveyors has been a continuous problem over a number of years. Numerous attempts have been made to alter skirt design and material, correct tracking issues and to reconfigure transfer points. See AARTS 2014-03573 for most recent issue with dust bogging the A14",
      "What happened?": "All 4 conveyors have carry back issues causing build up of alumina beneath the return run of the belt and particularly at the tail ends of the A15's.  The double dump valve from No1 DCD also tends to pass excessively when the valve flaps stick and this can cause either of the A14's to bog and trip.",
      "Requirement": "All product and dust should be contained within the confines of the belt, skirt boxes and dust collectors",
      "Obj. Evidence": "Clean up costs around the tail ends of the A15's are about $110k annually.; Clean up beneath the A14's can only be achieved by hosing and this results in sticky damp alumina causing wear of bearings, rollers, centring and tracking devices.; Uncontrolled flow of dust from the No1 DCD causes frequent spillage due to uneven belt loading and in worst case, bogging of a belt.",
      "Recom.Action": "Survey and repair all rollers and pulleys; Redesign and install new transfer points from A14 to A15; Revise A14 skirt installations with correct materials and positioning; Replace No1 DCD double dump valve with a small rotary valve",
      "Asset Number(s)": "CONVEYOR-KW050R-ALC15W,CONVEYOR-KW050R-ALC15E,CONVEYOR-KW050R-ALC14S,CONVEYOR-KW050R-ALC14N",
      "Amount of Loss": "110000($AUD)",
      "Immd. Contain. Action or Comments": "Continue house keeping actions around conveyors and maintain belt tracking as accurately as possible.",
      "Root Cause": "1 Continuous spillage around A14 and A15 conveyors; 2 Inadequate design of skirting, tracking and transfer arrangements; 3 Lack of discipline in root cause analysis and problem solving; 4 Conveyors are a critical bottleneck point for alumina transport and any decline in performance requires an equipment outage and / or tolerating product spillage; 5 No spare conveyor and little redundant capability; 6 Insufficient spare rollers (10 min/max) in stock to execute repairs - 86 day lead time on spares",
      "Action Plan": "Redesign A14 to A15 transfer points to ensure most efficient direction change of product flow with minimum loss of velocity | Survey pulleys and rollers on all four conveyors | Negotiate with roller supplier to keep more shelf stock for immediate supply | Redesign dust delivery system from No 1 DCD to A14's | Issue revised inspection and reporting format for conveyor inspections by fitters | Install revised transfer chute on A15W | Review and revise A14 skirts for correct positioning and appropriate skirt material | Install double dump valve replacement on No 1 DCD | Repair / replace defective rollers and pulleys | Install revised skirting system | Install revised transfer chute on A15E",
      "Due Date": "2015-01-05T00:00:00 | 2015-01-30T00:00:00 | 2015-02-20T00:00:00 | 2015-02-27T00:00:00 | 2015-04-17T00:00:00",
      "Complete": "Yes",
      "Completion Date": "2015-01-05T00:00:00 | 2015-01-30T00:00:00 | 2015-03-05T00:00:00",
      "Comments": "Curved chutes and access doors fabricated | Large number of rollers and pulleys on all conveyors defective | Sandvik have committed to hold 80 - 100 trough and return rollers in stock | Small Lisbon rotary valve to be installed linked to DCD hopper level instruments for speed control | Generic inspection sheet created in consultation with fitters and now issued against asset activities in eAM | Spillage and carry back much reduced. Air fluidisation also installed in dust chutes to prevent bogging - completely successful | Polyurethane skirting trialled successfully. 100 mm material to be installed in all units. | Some replaced and remainder in the plan for replacement with A14S belt and replacement of A15 C/W pulleys. | Trial completed successfully. Remaining skirts to be changed out in conjunction with other planned outages for belts. | Fabrication of chute parts completed and installation scheduled in the plan.",
      "Response Date": "2015-01-05T00:00:00",
      "Response Revision Date": null,
      "Did this action plan require a change to the equipment management strategy ?": "Yes",
      "If yes, are there any corrective actions to update the strategy in APSS, eAM, ASM and BOM as required ?": "Yes",
      "Is Resp Satisfactory?": "Yes",
      "Reason if not Satisfactory": "DATA_NOT_AVAILABLE",
      "Reviewed Date:": "2015-03-05T00:00:00",
      "Did this action plan require a change to the equipment management strategy ? (review)": "No",
      "If yes, APSS Doc #": null,
      "Asset Activity numbers": null,
      "Effectiveness Verification Due Date": "2015-04-09T00:00:00",
      "IsActionPlanEffective": "Yes",
      "Action Plan Eval Comment": "Changes have been partially effective and further work is required on skirting, pulleys and dust collectors to complete the project. Spillage is still excessive and no single change will resolve the issue particularly as many pulleys and rollers are defective and causing belt tracking issues.",
      "Action Plan Verification Date:": "2015-04-08T00:00:00",
      "_facility_name": "Kwinana-R1",
      "Root Cause Tail Extraction": "6 Insufficient spare rollers (10 min/max) in stock to execute repairs - 86 day lead time on spares"
    },

  


  
Chat




Unread
Channels
Chats

Has context menu
Unread messageLast messageGroup chatMeeting chatChatPersonal at mentionEveryone at mentionImportantUrgentDraftDraftMutedMeeting in progressMeet now in progressYou can't send messages because you are not a member of the chat.PrivateSharedHas context menuChannel at mentionTeam at mentionPersonal at mentionUnreadUnreadMeeting in progressUnreadChannelTeamHas pinned messagesSee moreCommunity
RCA - Progress update

Chat

Shared

Recap

Speaker Coach

Q&A

Meeting Whiteboard

Has context menu

2



Monday, June 23, 2025 2:00 pm - 2:55 pm

Share

Open in Stream

Content
No files were shared.

Notes

AI notes

Mentions

Transcript
Transcript. Use arrow keys to navigate between transcript entries.

bot
2/2

AI-generated content may be incorrect
DX

David XU
0 minutes 6 seconds0:06
David XU 0 minutes 6 seconds
Organised, maybe organise a meeting later.
David XU 0 minutes 10 seconds
I like her because OK.

Pervez, Ammar
0 minutes 15 seconds0:15
Pervez, Ammar 0 minutes 15 seconds
OK, let me see. So I just wanted to discuss what's happening.
Pervez, Ammar 0 minutes 23 seconds
Now, that's not what I am looking for.
Pervez, Ammar 0 minutes 27 seconds
Sent items to.
DX

David XU
0 minutes 39 seconds0:39
David XU 0 minutes 39 seconds
So how do we start about from the team the task or from the last week?
David XU 0 minutes 47 seconds
Summary report.

Pervez, Ammar
0 minutes 47 seconds0:47
Pervez, Ammar 0 minutes 47 seconds
Let's start from the teams tasks. Let's start from the team tasks and see where we are.
DX

David XU
0 minutes 49 seconds0:49
David XU 0 minutes 49 seconds
OK.
David XU 0 minutes 54 seconds
Yeah, maybe I can share my screen.

Pervez, Ammar
0 minutes 56 seconds0:56
Pervez, Ammar 0 minutes 56 seconds
Yes, please. Yeah.

Pervez, Ammar
16 minutes 48 seconds16:48
Pervez, Ammar 16 minutes 48 seconds
Can you? Yeah. Can you return action request numbers is my question because you you did not show me that you are returning action request number. You're showing me you are returning the files but not action request number, right? So you're returning file leave because I don't want to return filenames, I want to return.
DX
David XU
17 minutes17:00
David XU 17 minutes
Yes. No, no, no, no, actually.

Pervez, Ammar
17 minutes 10 seconds17:10
Pervez, Ammar 17 minutes 10 seconds
I give it a natural language.
Pervez, Ammar 17 minutes 14 seconds
Like, sorry, natural language query and it then returns me action request number not like if you write BR that you are just using a keyword search right? So that's not the intention. That's not what we are trying to do you we are we already have keyword search we want to have that's not virgin one virgin one should be you can ask a natural language query and then get a get.
DX
David XU
17 minutes 19 seconds17:19
David XU 17 minutes 19 seconds
Yeah.
David XU 17 minutes 25 seconds
Yes, yes.
David XU 17 minutes 31 seconds
Mm hmm.

Pervez, Ammar
17 minutes 39 seconds17:39
Pervez, Ammar 17 minutes 39 seconds
Our action request number now, whether that action request number is correct or not, that's version one.
Pervez, Ammar 17 minutes 44 seconds
Right. But you you cannot have version one without returning an action request number.
DX
David XU
17 minutes 44 seconds17:44
David XU 17 minutes 44 seconds
Yeah, yeah, yeah. OK.

Pervez, Ammar
17 minutes 51 seconds17:51
Pervez, Ammar 17 minutes 51 seconds
Like you can return multiple. Let's start with action request number that if you ask a simple query then I should get some action request numbers. OK how do you do that? That's where you need to design it. OK, I need to. I I'm giving you some one option was to break it into Jason files but you could also have it as a as a table so you keep everything as a table and then you run an SQL query on it. I don't know our.
DX
David XU
17 minutes 54 seconds17:54
David XU 17 minutes 54 seconds
Yeah.
David XU 17 minutes 58 seconds
Mm hmm.
David XU 18 minutes 2 seconds
OK, OK. Understand.
David XU 18 minutes 7 seconds
OK.

Pervez, Ammar
18 minutes 21 seconds18:21
Pervez, Ammar 18 minutes 21 seconds
So that's up to you. How do you keep your data in there? The thing that is required and this is where you need to design first without developing, you need to design OK version one. This is what I would design you experiment a little bit and then you say OK that's not working that's this is also designed this is this is what I want to see and this is what I think we discussed last time right that that you would work on this kind of thing but I don't want a search engine.
DX
David XU
18 minutes 26 seconds18:26
David XU 18 minutes 26 seconds
OK.
David XU 18 minutes 34 seconds
Mm hmm.
David XU 18 minutes 39 seconds
Yeah. OK.
David XU 18 minutes 42 seconds
Mm hmm. Mm hmm mm hmm.

Pervez, Ammar
18 minutes 48 seconds18:48
Pervez, Ammar 18 minutes 48 seconds
What I want is to return a proper request, so that's what we want. So not a keyword search. We don't want a keyword search. Obviously this is where we are using AI. So when you when you talk about topics.
Pervez, Ammar 19 minutes 1 second
That's not using AI, you're using bots, but not AI.
DX
David XU
19 minutes 1 second19:01
David XU 19 minutes 1 second
Mm hmm.

Pervez, Ammar
19 minutes 6 seconds19:06
Pervez, Ammar 19 minutes 6 seconds
So when you when you go to copilot agents.
DX
David XU
19 minutes 10 seconds19:10
David XU 19 minutes 10 seconds
Mm hmm.

Pervez, Ammar
19 minutes 11 seconds19:11
Pervez, Ammar 19 minutes 11 seconds
The only way you use AI from what my I know is conversational boosting. You're using bots, but you're not using AI, so we wanna use agent which is also using.
Pervez, Ammar 19 minutes 25 seconds
An LLM in the back end.
Pervez, Ammar 19 minutes 29 seconds
Or I don't want to use LLM but some kind of.
Pervez, Ammar 19 minutes 34 seconds
Semantic search is happening or some kind of other advanced technique is being applied to it not using bombs because when you're using this search, you're just going to a topic and then you're specified next steps to it, right? That's what you have done. You'll just specify next steps and it's just returning the name of the file, but that's nothing new. Is something that can go in and then say file #1 is OK, file #5 is OK, file number 7, and then you return file 5157, right?
DX
David XU
19 minutes 39 seconds19:39
David XU 19 minutes 39 seconds
Yeah, yeah.
David XU 19 minutes 47 seconds
Mm hmm mm hmm.
David XU 19 minutes 58 seconds
Mm hmm.

Pervez, Ammar
20 minutes 3 seconds20:03
Pervez, Ammar 20 minutes 3 seconds
That is what we want and this is what you experiment, yeah.
DX
David XU
20 minutes 4 seconds20:04
David XU 20 minutes 4 seconds
So.
David XU 20 minutes 7 seconds
OK, I understand. Actually this is not a simple.
David XU 20 minutes 12 seconds
Query you can see here we we have built an agent flow. Here we call the agent agent file content because already all the files here this is the data set under this name URL we can we can search it for the name or search it for the action request number I just add action request number on the data because it read all the file and pass the file.

Pervez, Ammar
20 minutes 18 seconds20:18
Pervez, Ammar 20 minutes 18 seconds
Mm hmm. OK.
Pervez, Ammar 20 minutes 24 seconds
OK.
DX
David XU
20 minutes 37 seconds20:37
David XU 20 minutes 37 seconds
And search the file.
David XU 20 minutes 39 seconds
This is the. This is the flow.
David XU 20 minutes 42 seconds
Is the age in the flow.

Pervez, Ammar
20 minutes 42 seconds20:42
Pervez, Ammar 20 minutes 42 seconds
But how do you philtre it? How do you philtre? What's the philtre area?
DX
David XU
20 minutes 47 seconds20:47
David XU 20 minutes 47 seconds
They're in here. They're array over here. Let me show you the first array currently is only just the contained. Use the keyword item. Item is the user query. For example, we ask, find it, find me the mining the mining. OK, the match just match the items from the from the from the data from the. From the data here.

Pervez, Ammar
21 minutes 8 seconds21:08
Pervez, Ammar 21 minutes 8 seconds
No, this is this is where, first of all, you need to break down your query into.
DX
David XU
21 minutes 14 seconds21:14
David XU 21 minutes 14 seconds
Yes, yes.

Pervez, Ammar
21 minutes 15 seconds21:15
Pervez, Ammar 21 minutes 15 seconds
Proper keywords and you do identify and then you need to search.
Pervez, Ammar 21 minutes 20 seconds
Within that, Jason, so you need to do more work on it before we call it V version one. This is not version one. It's not, yeah.
DX
David XU
21 minutes 26 seconds21:26
David XU 21 minutes 26 seconds
No, I know, but I. But I just want to show you what I have done to come the idea. Actually, I read as well read the SharePoint file and then use the.
David XU 21 minutes 38 seconds
Use to match the the. Currently. This is a very simple version, but actually this is the whole idea. It already have connected to the SharePoint and the related the data file here can see here and so just like you said we need to if we need to return the actual request, get the from the ground truth we need to do more actually because the ground truth how how we can.
David XU 22 minutes 4 seconds
Use the use the quarry. For example, we have other two key points.
David XU 22 minutes 10 seconds
And keyword from the user query when you just search the responding the content and either the correct the actual request number is that right?

Pervez, Ammar
22 minutes 20 seconds22:20
Pervez, Ammar 22 minutes 20 seconds
Yeah, yeah.
DX
David XU
22 minutes 23 seconds22:23
David XU 22 minutes 23 seconds
So. So actually, yeah, maybe we need to redesign this one, but actually this is the best basic flow I think maybe useful. But actually yeah, I need to do more work, have a have a better design before I do more develop. Is that OK?

Pervez, Ammar
22 minutes 39 seconds22:39
Pervez, Ammar 22 minutes 39 seconds
Yeah, exactly. Exactly. So this is not this is not returning what we want, right. So we what we're wanting and this is where you need to design this. So and the yeah.
DX
David XU
22 minutes 40 seconds22:40
David XU 22 minutes 40 seconds
Yeah, yeah.
Is this transcript useful?






Transcript
25 June 2025, 03:03am

Wei Liu   0:08
Yeah.
That's right. Yeah, yeah.
The classical mind said is if it's not broken, do not try to fix it.

Pervez, Ammar   0:20
Yeah, exactly. Exactly. And they do not. It's it's far too complex. I wouldn't say complex. It's far too retrofitted. Everything that the process has been done. So in the last 100 years, it has come to a point which is become so complex that in order to understand that system or ecosystem, it takes months. Or As for someone to come in and understand it, not because it's.

Wei Liu   0:26
Yeah.
Yeah.

Pervez, Ammar   0:47
Difficult as a theory, but because how it has been applied so this is where obviously AI thrives in in structure and there is no structure to how the operation works.

Wei Liu   0:50
Hmm.
Yeah.
Yeah.

Pervez, Ammar   1:02
Now we are trying to bring that like me and Peter. Peter has been at it for a while.
But you can't have a proper AI without a structure, so this is where I guess I this meeting is around the design of it and this is where the design part of any solution becomes very important is because we can identify what is there, what is.
What needs to be there for this solution to work if we don't have a design, then yes, we do have the technology, but we don't know what is needed from that operations and I guess this meeting that David has put together is to discuss three of the designs because.

Wei Liu   1:27
Yeah.
Yeah. OK.

Pervez, Ammar   1:43
My our last meeting.
Just to reiterate, we had a meeting a week ago or something and I discussed with David what I wanted and David?
Did not put in the design because I asked him to put the design and I I had to ask him again yesterday. So this I'm hoping that today we'll have a proper design of what is required was expected and then.
The feedback I'll I'll try to give feedback on whether that is the the functional requirement because the function because what what design that David put through yesterday wasn't as per the functional requirement that I gave him a week ago. So I wanna understand whether this designs event in three stage designs. So I wanna see what's the first, second and the third stage.

Xu, Jinguo (University of Western Australia)   2:31
Yes. Yeah, I have a basic idea. What we what about the big picture of the three stage so.
This is my understanding of the need of this task, how copilot studio agent can do. For example, if I have a user quarry this is. Maybe this is the case user quarry and this is the expected output.
And we need to consider scenes like this. First one, we need to power LLM. Power the agent. It should be generative orchestration. No topic and voice and then we should transfer the query, extract entity and transfer the entities to the sequel. And they use the sequel execute sequel to return the actual request number.
So, and here's the challenges. So we have the maybe the two challenges. One is the entities extraction.
And another is the transfer to the structure the sequel.
So what I'm understanding what I'm explore what the copilot studio agent at the first stage. Maybe we just focus on them already building in the features from the Copeland studio for example, we need to use the generative mode of this agent, not not the classical mode, because the classic mode maybe just.
Snorted. Flexible enough to get the results. Because and in my current version is the classical mode.
Just use the keywords match. It's not AAI, so I think we need to enable the generative mode. Is this correct Amma?

Pervez, Ammar   4:28
So what I understand about the copilot studio is.
You're you are just.
Using the generative mode to identify which topic you have to go to, right, so you still need to have and this is where the conversational boosting topic comes into the picture. The conversational boosting, basically.

Xu, Jinguo (University of Western Australia)   4:52
Yeah.

Pervez, Ammar   4:52
Neighbours that generated AI and that they the only thing that's different in a bot or an agent that.
That Co pilot makes is that either you specify a topic right and you specify what the next steps are, or you specify or you let them decide what the topic would be, and then you will still need to try to. Yeah. So.

Xu, Jinguo (University of Western Australia)   5:07
Yeah.
I mean just basically for example, this is a core right generative AI generative mode can't understand what's the question is if the classical mode we need to build a topic and trigger the topic and then this is manually created steps. If we don't have the generative AI and then we just.

Pervez, Ammar   5:18
Yeah.
Mm hmm.

Xu, Jinguo (University of Western Australia)   5:39
Configure the different search methods at this stage. If we manually created trigger this topic.
In the classical mode, so this is the difference and I think another difference if the generative mode I can understand understand the query because the way in the generative mode it have the building building features which understand the questions. But if the classical mode the the AI can't understand what what this user core is and what the task is, we need to manually trigger the topic and.

Pervez, Ammar   5:46
Mm hmm.
Mm hmm. OK. Yeah, yeah, yeah.

Xu, Jinguo (University of Western Australia)   6:15
Just follow the topic.
And generative answer for the topic. Yeah, this. What I'm I'm yeah. This is the kind of virgin classical mode of my agent. So if you. If we're needed to understand the question, we need to transfer to the generation mode and understand the question and.

Pervez, Ammar   6:36
OK.

Xu, Jinguo (University of Western Australia)   6:37
Another one is we need to use the database because database and have some building index and a vector embedding already have this one.
But if we use the SharePoint, we don't have the index and embedding and so it's better to use the database and it also database have very structured table in the in the in this format it can can be easy for the future search and also the this one is the because this is copilot studio agent this.
Licence doesn't include much ability.
If we have the Microsoft 306 five licence, it can provide that enhanced essential results. This is from the document I just.
This the citation for three so here.

Pervez, Ammar   7:32
Yeah, let's let's go back to the database part so.
If you.

Xu, Jinguo (University of Western Australia)   7:39
Just run that document over the Microsoft Copilot Studio documentation. I just downloaded this one and transferred to mark it down and this is a citation. If we have this one enhanced enhanced search results from the Microsoft.

Pervez, Ammar   7:42
Yeah, yeah.

Xu, Jinguo (University of Western Australia)   7:53
365 copilot licence so maybe this is another additional.

Pervez, Ammar   7:56
Hmm.

Xu, Jinguo (University of Western Australia)   7:59
Requirement to configure, but maybe at this stage we can consider this one at a later stage so.

Pervez, Ammar   8:05
But you do have that licence in in.
Your UWA tenant, right?

Xu, Jinguo (University of Western Australia)   8:15
I'm not sure, but I mean this one is.
I I I think I can. I can configure this one for the for the tester case, but actually if we I mean if we we use the actual use we need to have this one, is that right?

Pervez, Ammar   8:33
No, no, I think if you can go for copilot studio, that means you have a Microsoft 365 licence. You can't access copilot studio if you do not have a close Microsoft 365 licence.
For for for Elko, I understand that this is what the licence you need, but in UW you already have this licence. You can't have a copilot studio.

Xu, Jinguo (University of Western Australia)   8:55
No, currently I I'm I'm not using the UW I I applied.
Developer account for this. For this project it's not UWA account.

Pervez, Ammar   9:08
OK, so you so you don't get so my understanding was you already have copilot studio in UWA, you don't have a.

Xu, Jinguo (University of Western Australia)   9:09
OK, OK.
Don't have, don't have. I'm. I'm not. I can't access the copilot studio of UWA. So currently I'm using.
Developer account which has the access of the copilot studio.

Pervez, Ammar   9:32
OK, but then you should have exactly same capabilities as a Microsoft 365 licence, right?

Xu, Jinguo (University of Western Australia)   9:35
Is Anthony.
No, really I don't. I think I don't know how I'm ever check this one. I might check this one just later. So this basic idea, the stage 1, just use them.

Wei Liu   9:50
So sorry, I just clarify. Ewa has copilots but not copilot studio.

Xu, Jinguo (University of Western Australia)   9:57
Yes, yes.

Wei Liu   9:57
I think I think the David did ask and and they didn't really reply. I think at the moment I think he's just using his own subscription and then the centre will give him reimbursement.

Pervez, Ammar   10:12
OK, so so that would give him access to copilot studio, right? So if he already has. Yeah. OK. So.

Xu, Jinguo (University of Western Australia)   10:13
Big.

Wei Liu   10:19
Yes.
Yes. So he has called, he has access, but through his own personal subscription.

Pervez, Ammar   10:26
Oh, OK, OK.

Xu, Jinguo (University of Western Australia)   10:29
So let's let's continue. Let's give a little bit of quick. So this the first stage is mainly based on the building in features of the Co pilot studio agent. I can have some.
Index and vector embedding at the database and it can have intelligence search. Understanding the intent of the questions so.
Maybe not so accurate. The answer may be so accurate, so we need to check.
How about his accuracy based on the granitooth and then this stage 2?
We can.

Pervez, Ammar   11:05
Let's let's let can we stay at Stage 1 so.
Have you checked what the SharePoint can do? Because data was allowed to check whether we have access to it or not and that's a separate thing. Do we have instances provision that's beyond my?
What? What items I can provision? Have you checked in SharePoint? Because I from my perspective stage two could be database and Stage 1 is that you give me?

Xu, Jinguo (University of Western Australia)   11:28
Yes.

Pervez, Ammar   11:34
The instructions or configuration required to work at which SharePoint SharePoint.

Xu, Jinguo (University of Western Australia)   11:39
So the stages one we are working with the SharePoint is there right?

Pervez, Ammar   11:43
Yes.

Xu, Jinguo (University of Western Australia)   11:45
OK.
OK, we'll check this one. How? How about the the the the results for the SharePoint and not the database?

Pervez, Ammar   11:56
Yes, yes. So that's what.

Xu, Jinguo (University of Western Australia)   11:59
OK, OK, no problem.

Pervez, Ammar   12:00
'Cause. Look. Yeah, that's what we are using SharePoint so we can't have a data. So step one should be just SharePoint.

Xu, Jinguo (University of Western Australia)   12:09
OK, OK.

Pervez, Ammar   12:09
Step 2 is database maybe and I I don't think I can have it provisioned.
Frankly, I haven't used database before so I I'll have to see if we even use database in elcoa.
I think they do for other development, but I haven't use it so I wouldn't know.

Xu, Jinguo (University of Western Australia)   12:29
Mm hmm.

Wei Liu   12:32
Why? Why date of birth?

Pervez, Ammar   12:34
Yeah, that's what my yeah.

Xu, Jinguo (University of Western Australia)   12:35
Can have the index in that can do the indexes and do the vector embedding.

Wei Liu   12:45
Only one solution I I what's the cooperate database is that snowflake or or data breaks?

Xu, Jinguo (University of Western Australia)   12:47
Yeah.

Wei Liu   12:56
I I'm pretty sure a snowflake gives vector embedding as well.

Pervez, Ammar   13:04
So so the original intent of this of this this very, very targeted project was so that we can put stuff in SharePoint and get results out of it. That's the main intent because SharePoint is accessible to everyone. And so it's copilot see. So we want to assess. So that's one of the main functional requirement to use SharePoint and then see how the results are. So you can't like that's a basic functional requirement to use SharePoint.
We can't use database because that's your passing, so might as well just connect it to AI search for example, right? So that's also another step. That's something that already exploring in AI studio or AI Foundry, so database or vector search is a second step. Vector search is not the first step we want to use.
What is available in or what is the first step? So we I want to see is.
What can be configuration we can do so that we can search using SharePoint?

Xu, Jinguo (University of Western Australia)   14:07
OK.

Wei Liu   14:09
So between.
Between the search you actually need to store the embedding somewhere and that's why I think David is proposing dataverse as a way of as a vector store. Is that right David?

Pervez, Ammar   14:25
Yes.

Wei Liu   14:27
But this can be provided by AI foundry.

Pervez, Ammar   14:32
Yes.

Wei Liu   14:32
SharePoint is only for having you know Jason file or or documents.
In there, or maybe your CS lease and and etcetera, so those.
Can be stored in SharePoint, but SharePoint itself doesn't do vector storage.

Pervez, Ammar   14:51
Yes. And that's so so my function. So let let's let's take a couple of steps back. So the functional requirement is that we want to put so the original CSV file or the Excel file needs to be in a format, not Jason. It needs to be a format which can be searched.

Wei Liu   14:57
Yeah.
Yeah.

Pervez, Ammar   15:10
By what's available in copilot studio. So that's the basic first requirement. Now if the results are that that's what version one would be, we can't change it to database and that's what like.
What we should make sure, because it's not about Jason. It's not about the Excel file. The user does not care about it, they want the user care about is that we have access to SharePoint. Now we what the original intent of we talked about David last week was that we want to check what SharePoint can do, what we can achieve with the SharePoint and copilot studio if the intent was need to go for vector database because that's already the next step. So we can already use AI search. We can use ADI.

Wei Liu   15:49
OK.
Yeah.

Pervez, Ammar   15:55
Embedding 8002 embedding cohere embedding. We can do a lot of that stuff. So, but the that was the original intent of this version one. Now that's version one and that was the design part like look, this is what the design is and then we'll see what it is. Now. I don't think your target of 70% is is achievable.

Xu, Jinguo (University of Western Australia)   16:20
Yes.

Pervez, Ammar   16:20
Or 90 percentage is achievable, so I don't know why you gave those very high numbers. Now these are very high numbers and I wasn't even expecting those numbers because you would need to. These are very domain specific questions which I even I don't know. And the numbers you have put together are sorry, the ground truth you have put together is also something not coming from the SME. So we we do have to go to the SME but we have to go to the SME with the fact that look we can use the natural language in this Co partner studio.

Xu, Jinguo (University of Western Australia)   16:23
Yeah, just a just a example. Yeah. Yeah.
Yes.

Pervez, Ammar   16:51
And it's giving us results which are only 40% correct or it's only giving us results for simple queries and it's not giving so that's that should be the your first. No no, that's don't. That's not a requirement that I'm saying. I'm saying once you test it then you know what you're cutting you you cannot assess. There's no target or definition of done or acceptance criteria for stage one. I'm not asking for acceptance criteria.
What my basic requirement is if we put something in SharePoint.
And we have copilot showed you what can be achieved.
OK, that's the basic requirement. Step 2 could be using vector databases. Now that's something completely different that whether we can have vector databases or whether it's AI foundry, AI search or dataverse or data breaks, which is what are our two answer based question about the platform that operations has which is called L core data platform that's based on data break. So that's all there.
Already, but that's not what we are connecting to. Copaallet is not open to be connected to that database.
OK. So yeah, that's my point on the design now.
OK, Step 2 would be. I don't think database would be one thing that we'll be doing.

Xu, Jinguo (University of Western Australia)   18:16
Mm hmm mm hmm.

Pervez, Ammar   18:17
OK, this is stage 1. So have you done any? I'm guessing you haven't done any testing on the SharePoint then? Like what? What format works for SharePoint? What should the Jason be file look like? You know? I'm guessing you haven't done that because you've you're.

Xu, Jinguo (University of Western Australia)   18:34
In my first vision agent, actually we can read the Jason from the SharePoint and read the use the keywords to match the content and output of the title of the of the of the file under the link I just show you last time maybe.

Pervez, Ammar   18:54
No, no, that was what you showed me. Was that it? Had. This was a keyword search on the file name, right. So.

Xu, Jinguo (University of Western Australia)   19:00
Yes, he would search, but I mean I can't read the. Yeah, we can read the.

Pervez, Ammar   19:03
A file name.

Xu, Jinguo (University of Western Australia)   19:07
SharePoint Jason file in in this existing agent.

Pervez, Ammar   19:11
Yeah, but you didn't try to use natural language. You were using topics, right? So you're not using any generational, yeah.

Xu, Jinguo (University of Western Australia)   19:16
Yes, yes, yes, it's the classical mode, not not the generative, not the natural language. Understanding it's the classical.

Pervez, Ammar   19:25
Yes, that's what we want. So we, the user will not know about the keywords need to we ask and if the technically speaking, if I knew the file name then I wouldn't need that this solution right? Because there are 30,000 files I don't or I only 3000 files. The problem main problem is that we can't search for a file right so.
We are not solving any problem. It should give any. So you should have a natural. So you're going to use the same query. Give me all of the reports where gear failure happened in a bearing, right? And then I want to see five report numbers. You you haven't done that for SharePoint, right?
Now, what do we need to do for that? Yes, you can go for this SQL. That is what we discussed about and this is what I've I I have done before and I recommended that you look into it, but that's a separate thing. That's a next step where you're generating an SQL query. Now whether that is possible with with copilot or not. That's also something we need to. We need to explore, but I don't think you have explored.

Xu, Jinguo (University of Western Australia)   20:17
Yeah.
Yes.

Pervez, Ammar   20:33
Using copilot suite, your tool generate an SQL and then running it. I think we have gone in a slightly different.
Direction is this with copilot. I don't think this is with copilot.

Xu, Jinguo (University of Western Australia)   20:44
Yeah, this is a copilot. This conversational language understanding from the copilot. We we can customise this. The setting in the copilot we can. This is because I'm copilot studio. Have AI. Just a share. Maybe share the copilot. Studio. Give me a second. I just.

Pervez, Ammar   20:50
Mm hmm.
OK.

Xu, Jinguo (University of Western Australia)   21:07
So I mean this is another choice for us actually.
Can you? Can you grant me the share for my UW account?

Pervez, Ammar   21:21
No, I don't have.

Wei Liu   21:25
I'm I'm just reading the Microsoft Datawords stuff, so anything you you.

Pervez, Ammar   21:30
Mm hmm.

Wei Liu   21:34
Send into.
OneDrive SharePoint.
Are automatically stored in Microsoft database, so copilot studio, so files uploaded in copilot studio actually use Microsoft database, so it's it's not a separate thing. It seems to be.

Pervez, Ammar   21:46
Yeah.

Wei Liu   21:57
It's coming with.
OneDrive and SharePoint storage. That's how the data is managed.
Not just a file system, but it's a it's a dataverse is a like almost like a data lake that allows you to dump information into that system and dataverse itself already gave you.
That embeddings.
And indices. So semantic index.
Created through back team buildings in there.
Through, umm, the.
The internal vectorization process.

Pervez, Ammar   22:45
OK.

Wei Liu   22:45
So you don't have it. Yeah. You, you, you you can. You can already consume.
Data stored in OneDrive and SharePoint.
And even sales force.
ServiceNow confluence WOW, then desk. So all this information are already there. It's just a matter of how you.

Pervez, Ammar   23:06
Mm hmm.

Wei Liu   23:09
Orchestrate using copilot studio to make use of those data.

Pervez, Ammar   23:16
Basically what you're saying is, if I look at SharePoint, there would be a SharePoint document connector in database.

Wei Liu   23:23
Yeah. Yeah, yeah, yeah, yeah.
Yeah. So I think maybe the first stage is for.
David to explore, you know, searching the document repository.
Provide a semantic search, so rather than, you know, uh, talk too much about database. Database seems to be something sitting in the back end that stores all this information together.

Pervez, Ammar   24:00
OK, so that's a good insight. That's all kind of because I we haven't used copilot so and I haven't used database myself so.

Wei Liu   24:03
Yep.

Pervez, Ammar   24:09
If that's what, but I don't think David meant this. He was going for a different direction.

Wei Liu   24:15
Yeah, yeah.

Pervez, Ammar   24:15
Right. So now the thing that needs to so I I have selected the SharePoint document as one of the connector database.
But then would we be able to connect to a specific folder within SharePoint?
Which we what I'm understanding already would have affected vectors generated for it.

Wei Liu   24:42
Yeah, yeah. I think we should be able to and it then it's a matter of whether we can use our own embeddings or our own vectorization approach to do the search. And you know how how much of flexibility we can insert into the searching.
Performance.

Pervez, Ammar   25:08
OK.

Wei Liu   25:09
Yep.

Xu, Jinguo (University of Western Australia)   25:10
Yeah, we can connect to the extra searching maybe.
API we can support for the searching.

Wei Liu   25:21
Yeah, I think because all these tools are still reasonably new, I think let's just focus on.
Investigating, you know how the data can be consumed.
In stage one and then work out how well it does the consumption. So the other thing I was talking to David about is one way.
When he generate the ground truth questions.
It needs to be guided. It needs to have proper dimension modelling in order to create this ground truth data set. So we need to ask sensible questions rather than just, you know, pick out entities and combine them. That may not make sense. So that could be, you know another.
Important task.
Ask for for creating benchmark data set creating you know ground truth so we can verify what we retrieved is actually useful and relevant.
For that ebbed rage, yeah, that pace of yeah.

Pervez, Ammar   26:35
Up, yeah.

Xu, Jinguo (University of Western Australia)   26:38
The thing that this is task is also highly related to the customised Azure NLU. Here on my screen this is the.

Pervez, Ammar   26:48
David, you're talking about something else. So we to to your point where the ground truths, what we we just I asked David to make was.

Wei Liu   26:53
Mm hmm.

Pervez, Ammar   26:58
Was just for our initial pass. The ground truth should come from the SME, so the the current data set does not have.

Wei Liu   27:00
Yeah, yeah.

Pervez, Ammar   27:06
The the required.
Information for you to make a for you. Make the ground truth because what I'm when I'm when I'm looking at the down truth is how are users going to use it?

Wei Liu   27:11
Yeah.

Pervez, Ammar   27:21
Right. So they're going to ask certain kind of questions and that's something that's not coming from the data that should be coming from the user itself because we could generate ground truth. But that may or may not be what the user is using the system for. So now the only reason why I asked David to make it as a very short exercise to combine entity so that we can see how good multiple entities can be detected by this.

Wei Liu   27:22
Yeah, yeah, yeah, yeah.
Yeah.
Yeah.

Pervez, Ammar   27:48
Language.
For lack of better language understanding.
Algorithm within Co partner shoot here so that I can break it down into entities.
And when when it breaks, so that was just the initial intent, but so that we can take it to the stakeholders, the stakeholder is back. He was in a way for few weeks. So what we wanted to take him to him is like look, we can make make this question and then it getting this answer. But as soon as we make it a more complex, it's giving answers. So can you give us all of the questions that you ask and that would be better. So I'm not expecting David to come up with the answers or even I can come up with the answers.

Wei Liu   28:22
Yeah, yeah, yeah, that, yeah.

Pervez, Ammar   28:29
That's what the stakeholder to come with it, but this was just an thing to check for us internally until we go to the root cause. This is just a a couple of weeks of.
The validity for these ground truth, the actual ground truth will come from the user so.

Wei Liu   28:40
Yeah, yeah.
Yeah.

Pervez, Ammar   28:45
OK. No, thank you. We for sending this through, I saw you send through the e-mail. So. So basically this is what was what I was expecting when I put up the design. It's if if you are proposing dataverse we we can't just go for a new thing we we need to make sure that the work that's foundational requirement is which is to use SharePoint. Now database is connected to SharePoint is a separate thing which obviously we've picked up. That's good. Thank you. We I haven't used that and I didn't know he was using datab.

Wei Liu   29:03
Oh.

Pervez, Ammar   29:14
Yeah, that's we, we discussed it a week ago that I want. Dave, look at the function requirement before proposing what the solutions are. Yes, we know vector database, I mean you could propose knowledge graph for that matter because that's the best way you could.
Insights from but we we have to move that one by one. So OK. So I do have to leave for a meeting. But thank you for.

Wei Liu   29:32
Yeah.

Pervez, Ammar   29:40
Be for your input and David for setting it up. So like we mentioned. So David, if you can go back and see what the found a functional requirements are and then we can.
And then you see OK, how can database be connected? That's the next step.

Xu, Jinguo (University of Western Australia)   29:56
Mm hmm.

Pervez, Ammar   29:57
But yeah, but you can't just jump to vector databases because there's a lot of things out there. But I'll go is not relying a lot of them, so even I have to justify. OK, I need database I because of this reason and there's no other way we can do what what's allowed in Alcoa. So this is how it has to work that I have to prove every time I have to get a new solution or a new connect or a new API connected.

Wei Liu   30:12
Yeah, yeah.
Fully understand it's not your own laptop yet.

Pervez, Ammar   30:23
And that's what what I've been doing. So I'm.
Yeah. So I I have to move. OK? I have to prove that this is what I need and then they have to do the security review and then like, right now I am one of the few five or six people who have who can even connect SharePoint. None of the other people can connect SharePoint to copilot studio, and they're still running a because there's a lot of security concern on what data can be exploited or if it coerces systems can be exploited through copilot studio.

Wei Liu   30:27
Yeah.
Yeah.
Yeah.

Pervez, Ammar   30:53
If it's not secured enough.
So yeah, that's where where I'm coming from. So yeah, let's connect together and I'll.
Thanks, Veg and David cheers. See ya.

Wei Liu   31:05
Yeah. Yeah. So if, yeah, if you sent me, like, give me a few days warning of.

Xu, Jinguo (University of Western Australia)   31:06
Thank you, Emma.

Wei Liu   31:15
Joining a meeting then I will try to adjust my schedule to join meetings. Yeah. Yeah. So normally I would. My days are filled up quite quickly. But yeah, give me some prior warnings. Yeah, OK. All right. Talk to you later. Thanks so much. Yeah.

Pervez, Ammar   31:19
Yeah, OK, now, sure.
No, no, I understand. I understand it. Yeah, sure, sure. Cool. Thanks. Say, thanks, Evan. Cheers. Bye.

Xu, Jinguo (University of Western Australia)   31:34
See ya. See ya, Anna.

Wei Liu   31:34
Yeah, but thanks, David. Bye.

Xu, Jinguo (University of Western Australia)   31:36
Thank you. Thank you way.

Xu, Jinguo (University of Western Australia) stopped transcription
