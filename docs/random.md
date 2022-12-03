<h2>📖 Documentation: Random restaurant</h2>

Command manual:

```console
$ what-to-eat random --help

 Usage: what-to-eat random [OPTIONS]

 Finds random restaurant via Wolt API

╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --profile    -p      TEXT                                                             Profile name [default: None]                                                               │
│ --tag        -t      TEXT                                                             Tag [default: None]                                                                        │
│ --technique          [delivery_price|-delivery_price|rating|-rating|mix|-mix|random]  Technique: delivery_price, -delivery_price, rating, -rating, mix, -mix, random             │
│                                                                                       [default: EvaluateTechnique.MIX]                                                           │
│ --help                                                                                Show this message and exit.                                                                │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯

```

Random restaurant draw is a command that allows you to find a random restaurant from the list of restaurants available in your localization. The basic command is as follows:

```console
$ what-to-eat random
┏━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ 🍕 Krowarzywa Kraków ┃                                                 Kraków, ul. Sławkowska 8 🍕 ┃
┡━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│               Rating │                                                 Excellent (8 / 100 reviews) │
│                Price │                                                                          💰 │
│         Opening time │                                                               11:00 - 00:00 │
│              Website │      https://wolt.com/pl/pol/krakow/restaurant/krowarzywa-krakow-slawkowska │
│                Phone │                                                               +48 531777136 │
│            Estimates │                                                                  40 minutes │
│      Payment Methods │                                                                        Card │
│          Description │             W naszych restauracjach dostaniesz wyśmienite wegańskie burg... │
│                 Tags │ Burger, Vegetarian, Veggie burger, Vegan, Kebab, Wrap, Plant-based, Healthy │
└──────────────────────┴─────────────────────────────────────────────────────────────────────────────┘

```

By default the command uses the `mix` technique, which means that the restaurant is selected based on the rating and delivery price. The `mix` technique is the default one, but you can change it by using the `--technique` option.
The `--technique` option allows you to select one of the following techniques:

  * `delivery_price` - the restaurant with the lowest delivery price is selected
  * `-delivery_price` - the restaurant with the highest delivery price is selected
  * `rating` - the restaurant with the highest rating is selected
  * `-rating` - the restaurant with the lowest rating is selected
  * `mix` - the restaurant is selected based on the rating and delivery price
  * `-mix` - the restaurant is selected based on the rating and delivery price
  * `random` - the restaurant is selected totally randomly

The `mix` technique is the default one, but you can change it by using the `--technique` option:

```console
$ what-to-eat random --technique delivery_price
```

While randomly drawing restaurants you can limit possible results by using specified tag option:
```console
$ what-to-eat random --tag pizza
```

The following command will draw a random restaurant from the list of restaurants available in your localization, but only those that have the `pizza` tag.

<h2>⚙️ Options </h2>

| Option            | Description                                                                                                                                                                            | Example usage                           |
|-------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------|
| `--profile`, `-p` | Option used to set profile while drawing restaurants. By default the `default` profile is used.                                                                                        | `what-to-eat random -p work`            |
| `--tag`, `-t`     | Option used to is used to filter restaurants by their tags while drawing restaurant. Searching is case insensitive.                                                                    | `what-to-eat random -t italian`         |
| `--techique`      | Option is used to select the technique used to draw a random restaurant. The following techniques are available: `delivery_price, -delivery_price, rating, -rating, mix, -mix, random` | `what-to-eat random --technique random` |
