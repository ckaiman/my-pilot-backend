from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Mission
from .serializers import MissionSerializer

@api_view(['GET', 'POST'])
def mission_list(request):
    if request.method == 'GET':
        missions = Mission.objects.all()
        serializer = MissionSerializer(missions, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = MissionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

@api_view(['POST'])
def process_log(request):
    """
    Simulated Agentic Logger.
    Parses a log entry (like 'Mars Recon is finished') and updates the DB.
    """
    log_text = request.data.get('log', '').lower()
    missions = Mission.objects.all()
    
    updated_mission = None
    new_status = None
    
    # Simple Agent logic (simulating an LLM extract):
    for m in missions:
        if m.name.lower() in log_text:
            updated_mission = m
            break
            
    if "finished" in log_text or "complete" in log_text:
        new_status = "Completed"
    elif "ready" in log_text or "starting" in log_text:
        new_status = "In Progress"
        
    if updated_mission and new_status:
        old_status = updated_mission.status
        updated_mission.status = new_status
        updated_mission.save()
        return Response({
            'success': True,
            'message': f"Agent identified mission '{updated_mission.name}' and updated status to '{new_status}'.",
            'extraction': { 'mission': updated_mission.name, 'status': new_status },
            'thought_process': f"Matched log keywords against mission '{updated_mission.name}'. Map 'finished' to 'Completed'."
        })
    
    return Response({
        'success': False,
        'message': "Agent could not clearly identify a mission or status in that log.",
        'thought_process': "Scanned log text but found no matching mission names or status keywords."
    })

@api_view(['POST'])
def agent_query(request):
    """
    Simulated Agentic API endpoint.
    This is where your AI Agent (MCP/LangChain) would process the query.
    """
    query = request.data.get('query', '')
    
    # Placeholder for Agent logic:
    # 1. AI decides to query Postgres
    missions_count = Mission.objects.count()
    
    response_data = {
        'agent_response': f"I analyzed your request: '{query}'. I currently see {missions_count} missions in the system.",
        'thought_process': 'Decided to count missions in Postgres database to fulfill user request.',
        'status': 'success'
    }
    
    return Response(response_data)
