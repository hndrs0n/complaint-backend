from .prompt_strategy import PromptStrategy
from .topics.sumas_llevando_prompt import SumasLlevandoPrompt
from .restas_prestando_prompt import RestasPrestandoPrompt
from .comparacion_numeros_prompt import ComparacionNumerosPrompt
from .problemas_sumas_restas_prompt import ProblemasSumasRestasPrompt
from .anterior_posterior_prompt import AnteriorPosteriorPrompt
from .descomposicion_numeros_prompt import DescomposicionNumerosPrompt
from .patrones_numericos_prompt import PatronesNumericosPrompt
from .operaciones_combinadas_prompt import OperacionesCombinadasPrompt
# Importa las demás estrategias aquí

class PromptStrategyFactory:
    def __init__(self):
        self._strategies = {
            "sumas_llevando": SumasLlevandoPrompt,
            "restas_prestando": RestasPrestandoPrompt,
            "comparacion_numeros": ComparacionNumerosPrompt,
            "problemas_sumas_restas": ProblemasSumasRestasPrompt,
            "anterior_posterior": AnteriorPosteriorPrompt,
            "descomposicion_numeros": DescomposicionNumerosPrompt,
            "patrones_numericos": PatronesNumericosPrompt,
            "operaciones_combinadas": OperacionesCombinadasPrompt
            
        }

    def get_strategy(self, topic):
        Strategy = self._strategies.get(topic)
        if Strategy is None:
            raise ValueError(f"No se encuentra la estrategia para el tema {topic}")
        return Strategy()
