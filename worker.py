import time

from dotenv import load_dotenv

from hatchet_sdk import Context, Hatchet

load_dotenv()

hatchet = Hatchet(debug=True)


@hatchet.workflow(on_events=["send:text"])
class TextMom:
    @hatchet.step(timeout="10s")
    def generate_message(self):
        print(
            "starting step1",
            time.strftime("%H:%M:%S", time.localtime()),
        )
        return {
            "step1": "done",
        }

    @hatchet.step()
    def send_message(self):
        print(
            "starting step2",
            time.strftime("%H:%M:%S", time.localtime()),
        )
        return {
            "step2": "step2",
        }

    @hatchet.step(parents=["step1", "step2"])
    def step3(self, context: Context):
        print(
            "executed step3",
            time.strftime("%H:%M:%S", time.localtime()),
            context.workflow_input(),
            context.step_output("step1"),
            context.step_output("step2"),
        )
        return {
            "step3": "step3",
        }

    @hatchet.step(parents=["step1", "step3"])
    def step4(self, context: Context):
        print(
            "executed step4",
            time.strftime("%H:%M:%S", time.localtime()),
            context.workflow_input(),
            context.step_output("step1"),
            context.step_output("step3"),
        )
        return {
            "step4": "step4",
        }


worker = hatchet.worker("text-mom-worker")
worker.register_workflow(TextMom())
worker.start()
