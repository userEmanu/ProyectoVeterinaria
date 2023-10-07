document.addEventListener("DOMContentLoaded", () => {
  const url = '/ventasPorBimestral/';

  try {
    fetch(url)
      .then((response) => response.json())
      .then(data => {
        const nombresBimestres = data.resultados.map(item => item.nombre_bimestre);
        const ventas = data.resultados.map(item => item.porcentaje_crecimiento);
        const ganancias = data.resultados.map(item => item.total_pedidos);
        const clientes = data.resultados.map(item => item.clientes);

        // Configurar y renderizar el gráfico ApexCharts
        new ApexCharts(document.querySelector("#reportsChart"), {
          series: [
            {
              name: 'Ventas',
              data: ganancias
            },
            {
              name: 'Porcentaje De Ganancias',
              data:  ventas
            },
            {
              name: 'Clientes',
              data: clientes
            }
          ],
          chart: {
            height: 350,
            type: 'area',
            toolbar: {
              show: false
            },
          },
          markers: {
            size: 4
          },
          colors: ['#4154f1', '#2eca6a', '#ff771d'],
          fill: {
            type: "gradient",
            gradient: {
              shadeIntensity: 1,
              opacityFrom: 0.3,
              opacityTo: 0.4,
              stops: [0, 90, 100]
            }
          },
          dataLabels: {
            enabled: true
          },
          stroke: {
            curve: 'smooth',
            width: 2
          },
          xaxis: {
            type: 'categories',
            categories: ['Febrero', 'Abril', 'Junio', 'Agosto', 'Octubre', 'Diciembre']
          },
          tooltip: {
            x: {
              format: 'dd/MM/yy'
            },
          }
        }).render();
      })
      .catch(error => {
        console.log(error);
      });
  } catch (error) {
    console.log(error);
  }
});
