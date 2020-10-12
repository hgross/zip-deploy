# Plantuml diagrams
Contains plant-uml diagrams for documentation.

## Generate diagrams using docker
```bash
cat deployment.puml | docker run --rm -i think/plantuml -tpng > deployment-example.png
```