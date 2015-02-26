# User
## /user
GET (done)
```json
{
    "email": <string email>,
    "name": <string name>
}
```

POST (done)
```json
{
    "name": <string name>
}
```

# Campaigns
## /campaigns
GET (done)
```json
[
    {
        "id": <id>,
        "name": <string name>,
        "gm": <string user>,
        "token": <string access token>,
        "created_at": <datetime>,
        "updated_at": <datetime>,
        "players": [
            {
                "id": <id>,
                "name": <string>,
                "character_name": <string>,
                "email": <string>
            }...
        ],
        "current_session": {
            "id": <id>,
            "name": <string name>,
            "created_at": <datetime>,
            "updated_at": <datetime>
        }
    }...
]
```

POST (done)
```json
{
    "name": <string name>
}
```


## /campaigns/##
GET (done)
```json
{
    "id": <string uuid>,
    "name": <string name>,
    "gm": <string user>,
    "token": <string access token>,
    "created_at": <datetime>,
    "updated_at": <datetime>,
    "players": [
        {
            "id": <id>,
            "name": <string>,
            "character_name": <string>,
            "email": <string>,
            "created_at": <datetime>,
            "updated_at": <datetime>
        }..
    ],
    "current_session": {
        "id": <id>,
        "name": <string name>,
        "created_at": <datetime>,
        "updated_at": <datetime>
    }
}
```

POST (done)
```json
{
    "name": <string name>
}
```

DELETE (done)

## /campaigns/##/players
GET (done)
```json
[
    {
        "id": <id>,
        "name": <string>,
        "character_name": <string>,
        "email": <string>,
        "created_at": <datetime>,
        "updated_at": <datetime>
    }...
]
```

## /campaigns/##/players/##
GET (done)
```json
{
    "id": <id>,
    "name": <string>,
    "character_name": <string>,
    "email": <string>,
    "created_at": <datetime>,
    "updated_at": <datetime>
}
```

POST (done)
```json
{
    "character_name": <string>
}
```

DELETE (done)

## /campaigns/token
POST (done)
Adds player to a campaign with that token
```json
{
    "token": <string token>,
    "character_name": <string character name (optional)>
}
```

## /campaigns/##/token

DELETE (done)
regenerates the campaign token, can only be called by the owner.

## /campaigns/##/sessions
GET (done)
```json
[
    {
        "id": <id>,
        "name": <string name>,
        "created_at": <datetime>,
        "updated_at": <datetime>
    }...
]
```

POST (done)
```json
{
    "name": <string name>,
    "created_at": <datetime>,
    "updated_at": <datetime>
}
```

## /campaigns/##/sessions/##
GET (done)
```json
{
    "id": <id>,
    "name": <string name>,
    "created_at": <datetime>,
    "updated_at": <datetime>
}
```

POST (done)
```json
{
    "name": <string name>
}
```

DELETE (done)
note: only the current session can be deleted, and only if it's not on any transactions

## /campaigns/##/sessions/##/notes
GET (done)
```json
[
    {
        "id": <id>,
        "owner": <string name>,
        "name": <string name>,
        "note": <string in markdown>,
        "public": <boolean>
    }...
]
```

POST (done)
```json
{
    "name": <string name, optional>,
    "note": <string in markdown>,
    "public": <boolean, default=True>
}
```

## /campaigns/##/sessions/##/notes/##
GET (done)
```json
{
    "id": <id>,
    "owner": <string name>,
    "name": <string name>,
    "note": <string in markdown>,
    "public": <boolean>
}
```

POST (done)
``json
{
    "name": <string name, optional>,
    "note": <string in markdown, optional>,
    "public": <boolean, optional>
}
```

DELETE (done)

## /campaigns/##/encounters
GET
```json
[
    {
        "id": <id>,
        "name": <string name>,
        "created_at": <datetime>,
        "updated_at": <datetime>
    }...
]
```

POST
```json
{
    "name": <string name>
}
```

## /campaigns/##/encounters/##
GET
```json
{
    "id": <id>,
    "name": <string name>,
    "created_at": <datetime>,
    "updated_at": <datetime>
}
```

POST
```json
{
    "name": <string name>
}
```

DELETE

## /campaigns/##/encounters/##/items
GET
```json
[
    {
        "id": <id>,
        "name": <string>,
        "type": <string>,
        "price": <float>,
        "quantity": <int>,
        "sale_percent": <float>,
        "weight": <float>,
        "created_at": <datetime>,
        "updated_at": <datetime>
    }...
]
```

POST
```json
{
    "name": <string>,
    "type": <string>,
    "price": <float>,
    "quantity": <int>,
    "sale_percent": <float>,
    "weight": <float>,
}
```

## /campaigns/##/encounters/##/items/##
GET
```json
{
    "id": <id>,
    "name": <string>,
    "type": <string>,
    "price": <float>,
    "quantity": <int>,
    "sale_percent": <float>,
    "weight": <float>,
    "created_at": <datetime>,
    "updated_at": <datetime>
}
```

POST
```json
{
    "name": <string>,
    "type": <string>,
    "price": <float>,
    "quantity": <int>,
    "sale_percent": <float>,
    "weight": <float>
}
```

DELETE


## /campaigns/##/players/##/loot
see */loot

## /campaigns/##/players/##/loot/##
see */loot/##


## /campaigns/##/loot
see */loot

## /campaigns/##/loot/##
see */loot/##

## *#/loot
GET
```json
[
    {
        "id": <id>,
        "name": <string>,
        "type": <string>,
        "price": <float>,
        "quantity": <int>,
        "sale_percent": <float>,
        "weight": <float>,
        "owner": <string, player name or null>,
        "created_at": <datetime>,
        "updated_at": <datetime>,
        "transactions": [
            {
                "id": <id>,
                "session_id": <id>,
                "owner": <string>,
                "notes": <string>,
                "created_at": <datetime>,
                "updated_at": <datetime>
            }
        ]
    }...
]
```

POST
```json
{
    "name": <string>,
    "type": <string>,
    "price": <float>,
    "quantity": <int>,
    "sale_percent": <float>,
    "weight": <float>
}
```

## */loot/##
GET
```json
{
    "id": <id>,
    "name": <string>,
    "type": <string>,
    "quantity": <int>,
    "price": <float>,
    "sale_percent": <float>,
    "weight": <float>,
    "owner": <string, player name or null>,
    "created_at": <datetime>,
    "updated_at": <datetime>,
    "transactions": [
        {
            "id": <id>,
            "session_id": <id>,
            "owner": <string>,
            "notes": <string>,
            "price": <float>,
            "created_at": <datetime>,
            "updated_at": <datetime>
        }
    ]
}...
```

POST
```json
{
    "name": <string>,
    "type": <string>,
    "price": <float>,
    "quantity": <int>,
    "sale_percent": <float>,
    "weight": <float>,
    "owner": <string, player name or null>
}...
```

DELETE

## */loot/##/transactions
GET
```json
[
    {
        "id": <id>,
        "session_id": <id>,
        "owner": <string>,
        "notes": <string>
        "created_at": <datetime>,
        "updated_at": <datetime>
    }
]
```

POST

## */loot/##/transactions/##
GET
```json
{
    "id": <id>,
    "session_id": <id>,
    "owner": <string>,
    "notes": <string>,
    "created_at": <datetime>,
    "updated_at": <datetime>
}
```

POST
```json
{
    "session_id": <id>,
    "owner": <string>,
    "notes": <string>
}
```

DELETE

