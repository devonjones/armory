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
        "created": <datetime>,
        "updated": <datetime>,
        "players": [
            {
                "id": <id>,
                "name": <string>,
                "character_name": <string>,
                "email": <string>
            }...
        ]
    }...
]
```

POST (done)
```json
{
    "name": <string name>
}
```

## /campaigns/token
POST (done)
Adds player to a campaign with that token
```json
{
    "token": <string token>,
    "character_name": <string character name (optional)>
}
```

regenerates the campaign token, can only be called by the owner.

## /campaigns/##
GET (done)
```json
{
    "id": <string uuid>,
    "name": <string name>,
    "gm": <string user>,
    "token": <string access token>,
    "created": <datetime>,
    "updated": <datetime>,
    "players": [
        {
            "id": <id>,
            "name": <string>,
            "character_name": <string>,
            "email": <string>,
            "created": <datetime>,
            "updated": <datetime>
        }..
    ]
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
GET
```json
[
    {
        "id": <id>,
        "name": <string>,
        "character_name": <string>,
        "email": <string>,
        "created": <datetime>,
        "updated": <datetime>
    }...
]
```

POST
```json
{
    "name": <string>,
    "character_name": <string>,
    "email": <string>
}
```

## /campaigns/##/players/##
GET
```json
{
    "id": <id>,
    "name": <string>,
    "character_name": <string>,
    "email": <string>,
    "created": <datetime>,
    "updated": <datetime>
}
```

POST
```json
{
    "name": <string>,
    "character_name": <string>,
    "email": <string>
}
```

DELETE

## /campaigns/##/token

DELETE (done)
regenerates the campaign token, can only be called by the owner.








## /campaigns/##/sessions
GET
```json
[
    {
        "id": <id>,
        "name": <string name>,
        "created": <datetime>
    }...
]
```

POST
```json
{
    "name": <string name>,
    "created": <datetime>
}
```

## /campaigns/##/sessions/##
GET
```json
{
    "id": <id>,
    "name": <string name>,
    "created": <datetime>
}
```

POST
```json
{
    "name": <string name>
}
```

DELETE

## /campaigns/##/encounters
GET
```json
[
    {
        "id": <id>,
        "name": <string name>,
        "created": <datetime>,
        "updated": <datetime>
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
    "created": <datetime>,
    "updated": <datetime>
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
        "created": <datetime>,
        "updated": <datetime>
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
    "created": <datetime>,
    "updated": <datetime>
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
        "created": <datetime>,
        "updated": <datetime>,
        "transactions": [
            {
                "id": <id>,
                "session_id": <id>,
                "owner": <string>,
                "notes": <string>,
                "created": <datetime>,
                "updated": <datetime>
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
    "created": <datetime>,
    "updated": <datetime>,
    "transactions": [
        {
            "id": <id>,
            "session_id": <id>,
            "owner": <string>,
            "notes": <string>,
            "price": <float>,
            "created": <datetime>,
            "updated": <datetime>
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
        "created": <datetime>,
        "updated": <datetime>
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
    "created": <datetime>,
    "updated": <datetime>
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

