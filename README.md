# Knowledge Graph

Store all of your knowledge in one place, locally

## Purpose

When I set off on my software engineering journey, I tried my best to learn as many topics and
technologies as I can. Naturally, I've forgetten a lot of what I had previously learned. This
is due to multiple factors, but mainly not having timed repetition, as well as not being
able to connect the dots between topics at the time.

That's where this project comes in. You can create a connected graph of different categories
which all have associated topics and facts. You can quiz yourself to help refresh your
understanding of certain topics. Moreover, knowledge graph retains info on when you refreshed
different topics, and based on weak spots in your graph, can requiz you to ensure you always
remain sharp.

## How It Works

Each major category is a large node in the graph. The smaller topics underneath the category are
smaller nodes encircling it. Each large node has a score out of 100. With time, scores decrease.
In order to increase your score, you can take quizzes, which will see how you know about the given
topic. Depending on the result, the large node as well as encircling nodes will see their scores
shifted. This also reflects partially onto the score of neighbours. Thus, you can think of getting
the right answer as increasing a subset of node values, with the increment weakening as you
get further away from the relevant nodes.

## Tech Stack

Project built with Django. The db is sqlite, and all ml models are ran locally.

## Setup
