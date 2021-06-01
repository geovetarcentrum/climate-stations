function []=GVC_plot_english_v3(n,tendata)
%% Plot initialisation
startday=n-3;
X1=startday:10/1440:n+1;
plotdata=NaN(length(X1),size(tendata,2));
plotdata(:,1)=X1';
index=1;
for i=1:size(plotdata,1)
    line2=find(plotdata(i,1)==tendata(:,1));
    if line2>1
        if size(tendata,1)>index
            plotdata(i,:)=tendata(line2,:);
            index=index+1;
        end
    end
end

figure1 = figure('Position',[10 5 460 900],'color',[1 1 1]);

xlabels={'0',' ',' ','6',' ',' ','12',' ',' ','18',' ',' ','0'...
    ,' ',' ','6',' ',' ','12',' ',' ','18',' ',' ','0'...
    ,' ',' ','6',' ',' ','12',' ',' ','18',' ',' ','0'...
    ,' ',' ','6',' ',' ','12',' ',' ','18',' ',' ','0'};
xlabels2={' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '...
    ,' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '...
    ,' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '...
    ,' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '};

tsize=10;
ysize=10;
asize=8;

%% Temperature
Temp_ylim_lo = -15; Temp_ylim_up = 15;
axes1 = axes('Parent',figure1,...
    'YLim',[Temp_ylim_lo Temp_ylim_up],...
    'YTick',[-30 -25 -20 -15 -10 -5 0 5 10 15 20 25 30 35 40],...
    'YTickLabel',[-30 {''} -20 {''} -10 {''} 0 {''} 10 {''} 20 {''} 30 {''} 40],...
    'XLim',[n-3 n+1],...
    'Position',[0.12 0.89 0.85 0.07],...
    'FontSize',asize,...
    'XTickLabel',xlabels,...
    'XTick',n-3:1/12:n+1,...
    'TickLength',[0.005 0.1],...
    'YGrid','on');
box('on');
hold('all');
title('Air temperature','FontSize', tsize);
% plot6=plot(plotdata(:,1),plotdata(:,26),'r');
plot6=plot(plotdata(:,1),plotdata(:,5),'r');
ylabel('^oC','FontSize',ysize)

%% Dates labes
text(n-3+3.2,Temp_ylim_lo-0.34*(Temp_ylim_up - Temp_ylim_lo),datestr(n,29),'FontSize',asize)
text(n-3+2.2,Temp_ylim_lo-0.34*(Temp_ylim_up - Temp_ylim_lo),datestr(n-1,29),'FontSize',asize)
text(n-3+1.2,Temp_ylim_lo-0.34*(Temp_ylim_up - Temp_ylim_lo),datestr(n-2,29),'FontSize',asize)
text(n-3+0.2,Temp_ylim_lo-0.34*(Temp_ylim_up - Temp_ylim_lo),datestr(n-3,29),'FontSize',asize)

%% Humidity
axes2 = axes('Parent',figure1,...
    'YLim',[0 100],...
    'XLim',[n-3 n+1],...
    'Position',[0.12 0.76 0.85 0.07],...
    'FontSize',asize,...
    'YTickLabel',[0 25 50 75 100],...
    'YTick',0:25:100,...
    'XTickLabel',xlabels,...
    'XTick',n-3:1/12:n+1,...
    'TickLength',[0.005 0.1],...
    'YGrid','on');
box('on');
hold('all');
title('Relative humidity','FontSize', tsize);
% plot1=plot(plotdata(:,1),plotdata(:,27));
plot1=plot(plotdata(:,1),plotdata(:,6));
ylabel('%','FontSize',ysize);

%% Dates labes
%     text(n-3+3.2,-23,datestr(n,29),'FontSize',asize)
%     text(n-3+2.2,-23,datestr(n-1,29),'FontSize',asize)
%     text(n-3+1.2,-23,datestr(n-2,29),'FontSize',asize)
%     text(n-3+0.2,-23,datestr(n-3,29),'FontSize',asize)

%% Radiation - Shortwave
axes2 = axes('Parent',figure1,...
    'YLim',[0 1000],...
    'XLim',[n-3 n+1],...
    'Position',[0.12 0.64 0.85 0.07],...
    'FontSize',asize,...
    'XTickLabel',xlabels,...
    'XTick',n-3:1/12:n+1,...
    'TickLength',[0.005 0.1],...
    'YGrid','on');
box('on');
hold('all');
title('Incoming shortwave radiation','FontSize', tsize);
plot1=plot(plotdata(:,1),plotdata(:,[15 16]));
set(plot1(1),'DisplayName','Global','Color',[0 0 0],'LineStyle','-');
set(plot1(2),'DisplayName','Diffuse','Color',[1 0 0],'LineStyle','-');
%     set(plot1(3),'DisplayName','L ','Color',[0 0 1],'LineStyle','-');
legend1 = legend(axes2,'show');
set(legend1,'Position',[0.230 0.69 0.01 0.01],'Orientation','vertical','FontSize',8,...
    'FontName','Arial');
ylabel('W/m^2','FontSize',ysize);

%% Radiation - Longwave
axes2 = axes('Parent',figure1,...
    'YLim',[200 500],...
    'XLim',[n-3 n+1],...
    'Position',[0.12 0.52 0.85 0.07],...
    'FontSize',asize,...
    'XTickLabel',xlabels,...
    'XTick',n-3:1/12:n+1,...
    'TickLength',[0.005 0.1],...
    'YGrid','on');
box('on');
hold('all');
title('Incoming longwave radiation','FontSize', tsize);
plot1=plot(plotdata(:,1),plotdata(:,19));
ylabel('W/m^2','FontSize',ysize);
%     set(plot1,'XTickLabel',xlabels)

%% Pressure
axes3 = axes('Parent',figure1,...
    'YLim',[960 1040],...
    'XLim',[n-3 n+1],...
    'Position',[0.12 0.40 0.85 0.07],...
    'FontSize',asize,...
    'XTickLabel',xlabels,...
    'XTick',n-3:1/12:n+1,...
    'YTickLabel',[960 980 1000 1020 1040],...
    'YTick',960:20:1040,...
    'TickLength',[0.005 0.1],...
    'YGrid','on');
box('on');
hold('all');
title('Pressure','FontSize', tsize);
plot2=plot(plotdata(:,1),plotdata(:,28),'r');

ylabel('hPa','FontSize',ysize);

%% Windspeed
axes4 = axes('Parent',figure1,...
    'YLim',[0 20],...
    'YTick',[0 5 10 15 20 25 30],...
    'YTickLabel',[0 {''} 10 {''} 20 {''} 30],...
    'XLim',[n-3 n+1],...
    'Position',[0.12 0.28 0.85 0.07],...
    'FontSize',asize,...
    'XTickLabel',xlabels,...
    'XTick',n-3:1/12:n+1,...
    'TickLength',[0.005 0.1],...
    'YGrid','on');
box('on');
hold('all');
title('Wind speed','FontSize', tsize);
plot3=plot(plotdata(:,1),plotdata(:,35),'k');
ylabel('m/s','FontSize',ysize);

%% Wind direction
axes5 = axes('Parent',figure1,...
    'YLim',[0 360],...
    'XLim',[n-3 n+1],...
    'Position',[0.12 0.16 0.85 0.07],...
    'FontSize',asize,...
    'XTickLabel',xlabels,...
    'YTickLabel',[0 90 180 270 360],...
    'YTick',0:90:360,...
    'XTick',n-3:1/12:n+1,...
    'TickLength',[0.005 0.1],...
    'YGrid','on');
box('on');
hold('all');
title('Wind direction','FontSize', tsize);
%text(n-3+1,15,'CURRENTLY UNAVAILABLE')
plot4=plot(plotdata(:,1),plotdata(:,36));
set(plot4,'Color',[0 0 1],'LineStyle','none','Marker','.','Markersize',5);
ylabel('deg ( ^o )','FontSize',ysize);

%% Precipitation
axes6 = axes('Parent',figure1,...
    'YLim',[0 3],...
    'XLim',[n-3 n+1],...
    'Position',[0.12 0.04 0.85 0.07],...
    'FontSize',asize,...
    'YTickLabel',[0 1 2 3],...
    'YTick',0:1:3,...
    'XTickLabel',xlabels,...
    'XTick',n-3:1/12:n+1,...
    'TickLength',[0.005 0.1],...
    'YGrid','on');
box('on');
hold('all');
title('Precipitation','FontSize', tsize);
plot5=bar(plotdata(:,1),plotdata(:,31)/6,'r','EdgeColor',[1 0 0]);
set(plot5(1),'DisplayName','Precipitation');
ylabel('mm/10min','FontSize',ysize);
xlabel('Time (h)','FontSize',ysize);

%% Dates labes
text(n-3+3.2,-11.8,datestr(n,29),'FontSize',asize)
text(n-3+2.2,-11.8,datestr(n-1,29),'FontSize',asize)
text(n-3+1.2,-11.8,datestr(n-2,29),'FontSize',asize)
text(n-3+0.2,-11.8,datestr(n-3,29),'FontSize',asize)
%% Save graphs for web
% i1=num2str(2011);i2=num2str(08,'%2.2d');i3=num2str(01,'%2.2d');i4=num2str(23,'%2.2d');
% savtitle=['GVC_roof_',i1,i2,i3,'T',i4,'5734.png'];
savtitle=['GVC_roof_',datestr(round(now),30),'.png'];
PlotDir=fullfile('C:\MeteorologicalMeasurements\GVCroof\Plot\Figures');
figurea=fullfile(PlotDir,savtitle);
%     saveas(figure (1), figurea)
set(figure1,'PaperPositionMode','auto')
print(figure1,'-dpng',figurea)
%     d=getframe(figure1);
%     imwrite(d.cdata, figurea)
%     pause(10)
webtitle='GVC_plot.png';
PlotDir1=fullfile('C:\MeteorologicalMeasurements\GVCroof\Plot');
figurea1=fullfile(PlotDir1,webtitle);
%     saveas(figure (1), figurea1);
%     set(figure1,'PaperPositionMode','auto')
print(figure1,'-dpng',figurea1)
%     d=getframe(figure1);
%     imwrite(d.cdata, figurea1)
%     pause(10)
f=ftp('pc70.gvc.gu.se','urban-net');
cd(f,'public_html');
mput(f,'GVC_plot.png');


% Tablefigure
last=size(tendata,1);
fsize=5;
figure2 = figure('Position',[500 200 294 120],'color',[1 1 1]);
annotation(figure2,'textbox',[0.00 0.93 0.85 0.1],...
    'String',['Last downloaded data at: ' datestr(tendata(last,1),'mmmm dd, yyyy HH:MM') ' (CET)'],...
    'LineStyle','none','FontName','Verdana','FontSize',fsize,'FontWeight','bold');
annotation(figure2,'textbox',[0.00 0.03 0.85 0.9],...
    'String',{'Air Temperature:'
    'Relative humidity:'
    'Wind speed:'
    'Wind direction:'
    'Pressure (75 masl):'
    'Precepitation (rain):'
    'Accumulated rainfall (24 h):'
    'Global radiation:'
    'Diffuse radiation:'
    'Incoming longwave radiation:'},...
    'LineStyle','none','FontName','Verdana','FontSize',fsize);
if last > 144
annotation(figure2,'textbox',[0.55 0.03 0.85 0.9],...
    'String',{num2str(tendata(last,26),'%6.1f')
    num2str(tendata(last,27),'%6.1f')
    num2str(tendata(last,35),'%6.1f')
    num2str(tendata(last,36),'%6.1f')
    num2str(tendata(last,28),'%6.1f')
    num2str(tendata(last,31)/6,'%6.0f')
    num2str(sum(tendata(last-144:last,31))/6,'%6.1f')
    num2str(tendata(last,15),'%6.1f')
    num2str(tendata(last,16),'%6.1f')
    num2str(tendata(last,19),'%6.1f')},...
    'LineStyle','none','FontName','Verdana','FontSize',fsize,'FontWeight','bold');
else
   annotation(figure2,'textbox',[0.55 0.03 0.85 0.9],...
    'String',{num2str(tendata(last,26),'%6.1f')
    num2str(tendata(last,27),'%6.1f')
    num2str(tendata(last,35),'%6.1f')
    num2str(tendata(last,36),'%6.1f')
    num2str(tendata(last,28),'%6.1f')
    num2str(tendata(last,31)/6,'%6.0f')
    'NA'
    num2str(tendata(last,15),'%6.1f')
    num2str(tendata(last,16),'%6.1f')
    num2str(tendata(last,19),'%6.1f')},...
    'LineStyle','none','FontName','Verdana','FontSize',fsize,'FontWeight','bold');
 
end
    num2str(sum(tendata(:,10)),'%6.1f')
annotation(figure2,'textbox',[0.73 0.03 0.85 0.9],...
    'String',{' °C'
    ' %'
    ' m/s'
    ' °'
    ' hPa'
    ' mm/10 min'
    ' mm/24 h'
    ' W/m^2'
    ' W/m^2'
    ' W/m^2'},...
    'LineStyle','none','FontName','Verdana','FontSize',fsize);

fty3 = [0.9 0.79 0.68 0.57 0.46 0.35 0.24 0.13 0.02 -0.09];
fsize = 5.5;
figure3 = figure('Position',[500 200 294 130],'color',[1 1 1]);
set(gca,'Visible','off')
text(-0.13, 1.02, ['Last downloaded data at: ' datestr(tendata(last,1),'mmmm dd, yyyy HH:MM') ' (CET)'],...
    'FontName','Verdana','FontSize',fsize,'FontWeight','bold');
text(-0.13, fty3(1), 'Air Temperature:','FontName','Verdana','FontSize',fsize);
text(-0.13, fty3(2), 'Relative humidity:','FontName','Verdana','FontSize',fsize);
text(-0.13, fty3(3), 'Wind speed:','FontName','Verdana','FontSize',fsize);
text(-0.13, fty3(4), 'Wind direction:','FontName','Verdana','FontSize',fsize);
text(-0.13, fty3(5), 'Pressure (75 masl):','FontName','Verdana','FontSize',fsize);
text(-0.13, fty3(6), 'Precepitation (rain):','FontName','Verdana','FontSize',fsize);
text(-0.13, fty3(7), 'Accumulated rainfall (24 h):','FontName','Verdana','FontSize',fsize);
text(-0.13, fty3(8), 'Global radiation:','FontName','Verdana','FontSize',fsize);
text(-0.13, fty3(9), 'Diffuse radiation:','FontName','Verdana','FontSize',fsize);
text(-0.13, fty3(10), 'Incoming longwave radiation:','FontName','Verdana','FontSize',fsize);
if last > 144
text(0.65, fty3(1), num2str(tendata(last,26),'%6.1f'),'FontName','Verdana','FontSize',fsize,'FontWeight','bold');
text(0.65, fty3(2), num2str(tendata(last,27),'%6.1f'),'FontName','Verdana','FontSize',fsize,'FontWeight','bold');
text(0.65, fty3(3), num2str(tendata(last,35),'%6.1f'),'FontName','Verdana','FontSize',fsize,'FontWeight','bold');
text(0.65, fty3(4), num2str(tendata(last,36),'%6.1f'),'FontName','Verdana','FontSize',fsize,'FontWeight','bold');
text(0.65, fty3(5), num2str(tendata(last,28),'%6.1f'),'FontName','Verdana','FontSize',fsize,'FontWeight','bold');
text(0.65, fty3(6), num2str(tendata(last,31)/6,'%6.1f'),'FontName','Verdana','FontSize',fsize,'FontWeight','bold');
text(0.65, fty3(7), num2str(sum(tendata(last-144:last,31))/6,'%6.1f'),'FontName','Verdana','FontSize',fsize,'FontWeight','bold');
text(0.65, fty3(8), num2str(tendata(last,15),'%6.1f'),'FontName','Verdana','FontSize',fsize,'FontWeight','bold');
text(0.65, fty3(9), num2str(tendata(last,16),'%6.1f'),'FontName','Verdana','FontSize',fsize,'FontWeight','bold');
text(0.65, fty3(10), num2str(tendata(last,19),'%6.1f'),'FontName','Verdana','FontSize',fsize,'FontWeight','bold');
else
text(0.65, fty3(1), num2str(tendata(last,26),'%6.1f'),'FontName','Verdana','FontSize',fsize,'FontWeight','bold');
text(0.65, fty3(2), num2str(tendata(last,27),'%6.1f'),'FontName','Verdana','FontSize',fsize,'FontWeight','bold');
text(0.65, fty3(3), num2str(tendata(last,35),'%6.1f'),'FontName','Verdana','FontSize',fsize,'FontWeight','bold');
text(0.65, fty3(4), num2str(tendata(last,36),'%6.1f'),'FontName','Verdana','FontSize',fsize,'FontWeight','bold');
text(0.65, fty3(5), num2str(tendata(last,28),'%6.1f'),'FontName','Verdana','FontSize',fsize,'FontWeight','bold');
text(0.65, fty3(6), num2str(tendata(last,31)/6,'%6.1f'),'FontName','Verdana','FontSize',fsize,'FontWeight','bold');
text(0.65, fty3(7), 'NA','FontName','Verdana','FontSize',fsize,'FontWeight','bold');
text(0.65, fty3(8), num2str(tendata(last,15),'%6.1f'),'FontName','Verdana','FontSize',fsize,'FontWeight','bold');
text(0.65, fty3(9), num2str(tendata(last,16),'%6.1f'),'FontName','Verdana','FontSize',fsize,'FontWeight','bold');
text(0.65, fty3(10), num2str(tendata(last,19),'%6.1f'),'FontName','Verdana','FontSize',fsize,'FontWeight','bold');
end
text(0.85, fty3(1), '°C','FontName','Verdana','FontSize',fsize);
text(0.85, fty3(2), '%','FontName','Verdana','FontSize',fsize);
text(0.85, fty3(3), 'm/s','FontName','Verdana','FontSize',fsize);
text(0.85, fty3(4), '°','FontName','Verdana','FontSize',fsize);
text(0.85, fty3(5), 'hPa','FontName','Verdana','FontSize',fsize);
text(0.85, fty3(6), 'mm/10 min','FontName','Verdana','FontSize',fsize);
text(0.85, fty3(7), 'mm/24 h','FontName','Verdana','FontSize',fsize);
text(0.85, fty3(8), 'W/m^2','FontName','Verdana','FontSize',fsize);
text(0.85, fty3(9), 'W/m^2','FontName','Verdana','FontSize',fsize);
text(0.85, fty3(10), 'W/m^2','FontName','Verdana','FontSize',fsize);

webtitle='GVCtable_plot.png';
PlotDir1=fullfile('C:\MeteorologicalMeasurements\GVCroof\Plot');
figurea2=fullfile(PlotDir1,webtitle);

set(figure3,'PaperPositionMode','auto')
%     saveas(figure (2), figurea2)
print(figure3,'-dpng',figurea2)

f=ftp('pc70.gvc.gu.se','urban-net');
cd(f,'public_html');
mput(f,'GVCtable_plot.png');
