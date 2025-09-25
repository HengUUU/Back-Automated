import json
from pathlib import Path
from app.models.factories_info_model import Factory

FACTORY_FILE = Path(__file__).parent.parent / "/app/app/data" / "real_factory_info.json"
print(FACTORY_FILE.resolve())
print("Exists?", FACTORY_FILE.exists())

def load_factories():
    if not FACTORY_FILE.exists():
        return []
    with open(FACTORY_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_factories(factories: list):
    with open(FACTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(factories, f, ensure_ascii=False, indent=2)


def add_factory(factory: Factory):
    factories = load_factories()
    if any(f["name"] == factory.name for f in factories):
        raise ValueError("Factory with this name already exists")
    factories.append(factory.dict())
    save_factories(factories)
    return factory.dict()


def update_factory_by_name(name: str, factory_update):
    factories = load_factories()
    for i, f in enumerate(factories):
        if f["name"].lower() == name.lower():
            # only include fields the client actually sent
            update_data = factory_update.dict(exclude_unset=True)

            # merge the update into the existing record
            factories[i].update(update_data)

            save_factories(factories)
            return factories[i]

    raise ValueError("Factory not found")



def delete_factory_by_name(name: str):
    factories = load_factories()
    for i, f in enumerate(factories):
        if f["name"].lower() == name.lower():
            factories.pop(i)
            save_factories(factories)
            return
    raise ValueError("Factory not found")


def search_factories_by_name(name: str):
    factories = load_factories()
    name_lower = name.lower()
    return [f for f in factories if name_lower in f["name"].lower()]


