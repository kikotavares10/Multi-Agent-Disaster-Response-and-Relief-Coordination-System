import asyncio
from agentes import ResponderAgent, CivilianAgent, SupplyVehicleAgent, ShelterAgent, DepotAgent
from ambiente import Environment

async def main():
    # Inicializar o ambiente
    env = Environment(size=10)

    # Criar veículos de suprimento
    supply_vehicle_positions = [[1, 1], [8, 9], [8, 8], [4, 0]]
    supply_vehicles = []

    # Criar os veículos com os recursos especificados
    initial_resources = [
        {"agua_comida": 60,  "medicamentos": 60,  "combustivel": 100},  # Veículo 1
        {"agua_comida": 00,  "medicamentos": 40,  "combustivel": 100},  # Veículo 2
        {"agua_comida": 00,  "medicamentos": 20,  "combustivel": 4},
        {"agua_comida": 00,  "medicamentos": 0,  "combustivel": 100}
    ]

    for i, (position, resources) in enumerate(zip(supply_vehicle_positions, initial_resources), start=1):
        vehicle_jid = f"supply_vehicle{i}@localhost"
        supply_vehicle = SupplyVehicleAgent(vehicle_jid, "password", position, env)

        # Configurar os recursos iniciais do veículo
        supply_vehicle.recursos = resources

        await supply_vehicle.start()
        supply_vehicles.append(supply_vehicle)

    # Criar o depósito central
    depot_position = [0, 0]  # Posição inicial do depósito
    depot_resources = {"agua": 500, "comida": 500, "medicamentos": 300, "bens": 200, "combustivel": 1000}
    depot = DepotAgent("depot@localhost", "password", depot_position, depot_resources)
    await depot.start()

    # Criar os abrigos com capacidades e posições diferentes
    shelter1_position = [7, 7]
    shelter1 = ShelterAgent("shelter1@localhost", "password", shelter1_position, len(supply_vehicle_positions))
    await shelter1.start()

    shelter2_position = [5, 5]
    shelter2 = ShelterAgent("shelter2@localhost", "password", shelter2_position, len(supply_vehicle_positions))
    await shelter2.start()

    # Atualiza o mapa para incluir os abrigos
    env.move_agent(shelter1_position, shelter1_position, agent_type=5)  # Representa o Shelter 1
    env.move_agent(shelter2_position, shelter2_position, agent_type=5)  # Representa o Shelter 2

    # Simulação
    print("\nMapa inicial da cidade:")
    env.print_city_map()

    print("\nIniciando simulação de 60 segundos...")

    # Evento 1: Abrigos esgotam seus recursos
    await asyncio.sleep(5)
    print("\n[Evento] Shelter 1 esgota seus recursos.")
    shelter1.agua_comida = 0
    #shelter2.medicamentos = 0
    print("Shelter 1 agora sem água e comida.")

    await asyncio.sleep(12)
    print("\n[Evento] Shelter 2 esgota seus recursos.")
    shelter2.agua_comida = 0
    shelter2.medicamentos = 0
    print("Shelter 2 agora sem água e medicamentos.")

    # Espera até o fim da simulação
    await asyncio.sleep(50)
    print("\nFim da simulação de 60 segundos")

    # Finalizar agentes
    await shelter1.stop()
    await shelter2.stop()
    for vehicle in supply_vehicles:
        await vehicle.stop()
    await depot.stop()

    print("\nEstado final do mapa:")
    env.print_city_map()

if __name__ == "__main__":
    asyncio.run(main())
