# graphql_python_example

Challenge #1 : Familiarizing yourself with Graphql Queries and Mutations 
---------------
For this challenge, you are going to :
1. Find Events greater than 100, less than 121 with a description that has the letter "a" and "e" in it.
2. You will create a new user. You will create a few roles and and event for that user. Once you are done, you will delete some of the roles and events you created for that user, but not all of them. 

Example Queries:
Example 1: Get Event by Id 11
```bash
{
  events(where:{id:11})
  {
    edges
    {
      node
      {
        id
        createdBy
      }
    }
  }
}
```

Example 2: Get User with a Name like Joe and ID greater than 4:
```bash
{
  users(where:{idGt:4, nameLike:"%Joe%"})
  {
    edges
    {
      node
      {
        id
        name
        events
        {
          edges
          {
            node
            {
              id
            }
          }
        }
        roles
        {
          edges
          {
            node
            {
              id
            }
          }
        }
      }
    }
  }
}
```

Mutation: 
Create Example:
```bash
mutation{
  createEvent(createdBy:3, description:"ahh", name:"wee")
  {
    event
    {
      id
      name
      description
      createdBy

    }
  }
}
```

Update Example:
```bash
mutation{
  updateUser(email:"dshonaike41@gmail.com", name:"ahh", roleIds:[5,4,6], id:103 )
  {
    user
    {
      id
      email
      roles
      {
        edges
        {
          node
          {
            id
          }
        }
      }
    }
  }
}
```

Delete Example:
```bash
mutation{
  deleteUser(id:103)
  {
    userId
  }
}
```
Getting started if you want this repo locally
---------------
To run locally, you will need to have Python3, Pip3, Postgres, Docker, and Docker-Compose installed.
First you'll need to get the source of the project. Do this by cloning the repository:

```bash
# Get the example project code
git clone https://github.com/spicylola/graphql_python_example.git
cd graphql_python_example.git
```

```bash
# Create a virtualenv in which we can install the dependencies
virtualenv venv
source venv/bin/activate
```

Now we can install our dependencies:

```bash
pip install -r requirements.txt
```
Make sure Docker is running.

Now the following command will setup the database and run the server:

```bash
docker-compose up -d

flask db upgrade
flask load_seed_events
flask load_seed_roles
flask load_seed_users
flask run

```


Now head on over to
[http://127.0.0.1:5000/graphql](http://127.0.0.1:5000/graphql)
and run some queries!




