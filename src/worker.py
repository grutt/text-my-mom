import time

from dotenv import load_dotenv

from hatchet_sdk import Context, Hatchet

load_dotenv()

hatchet = Hatchet(debug=True)


@hatchet.workflow(on_events=["send:text"])
class TextMom:
    @hatchet.step(timeout="10s")
    def generate_message(self, context):
        print(
            "starting step1",
            time.strftime("%H:%M:%S", time.localtime()),
        )
        return {
            "step1": "done",
        }

    @hatchet.step(parents=["generate_message"], timeout="10s")
    def send_message(self, context):
        print(
            "starting step2",
            time.strftime("%H:%M:%S", time.localtime()),
        )
        return {
            "step2": "step2",
        }

def main():
    worker = hatchet.worker("text-mom-worker")
    worker.register_workflow(TextMom())
    worker.start()
